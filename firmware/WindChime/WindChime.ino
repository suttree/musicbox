#include <Arduino.h>
#include <ESP_I2S.h>
#include <esp_random.h>

#include "ChimeEngine.h"

#ifndef MUSICBOX_USE_RTC
#define MUSICBOX_USE_RTC 0
#endif

#if MUSICBOX_USE_RTC
#include <RTClib.h>
#include <Wire.h>
#endif

namespace {
constexpr int bitClockPin = 4;
constexpr int wordSelectPin = 5;
constexpr int audioDataPin = 6;
constexpr std::size_t framesPerBlock = 256;

I2SClass audio;
int16_t samples[framesPerBlock];
int16_t stereo[framesPerBlock * 2];
bool audioReady = false;

#if MUSICBOX_USE_RTC
constexpr int clockDataPin = 8;
constexpr int clockSignalPin = 9;
constexpr uint8_t clockAddress = 0x68;
bool clockBusReady = false;
uint32_t lastClockRead = 0;

uint8_t fromBcd(uint8_t value) {
    return 10 * (value >> 4) + (value & 0x0f);
}

bool withinPlaybackHours() {
    // Read time and the oscillator-stop flag in one transaction.
    uint8_t registers[16];
    Wire.beginTransmission(clockAddress);
    Wire.write(0);
    if (Wire.endTransmission(false) != 0
        || Wire.requestFrom(clockAddress, sizeof(registers)) != sizeof(registers)) {
        return false;
    }
    for (auto& value : registers) {
        value = Wire.read();
    }
    const uint8_t month = fromBcd(registers[5] & 0x1f);
    if ((registers[15] & 0x80) || (registers[2] & 0x40) || (registers[5] & 0x80)
        || month < 1 || month > 12) {
        return false;
    }
    const DateTime time(2000 + fromBcd(registers[6]), month,
                        fromBcd(registers[4]), fromBcd(registers[2]),
                        fromBcd(registers[1]), fromBcd(registers[0]));
    if (!time.isValid()) {
        return false;
    }
    const int hour = time.hour();
    const int day = time.dayOfTheWeek();
    const bool weekend = day == 0 || day == 6;
    return (hour >= 6 && hour < 9) || (hour >= 18 && hour < 23)
        || (weekend && hour >= 12 && hour < 14);
}
#endif
}

void setup() {
    Serial.begin(115200);
    audio.setPins(bitClockPin, wordSelectPin, audioDataPin);
    audioReady = audio.begin(I2S_MODE_STD, ChimeEngine::sampleRate,
                             I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO);
    if (!audioReady) {
        Serial.println("Could not start I2S audio.");
        return;
    }

#if MUSICBOX_USE_RTC
    clockBusReady = Wire.begin(clockDataPin, clockSignalPin);
    if (clockBusReady) {
        Wire.setTimeOut(5);
    } else {
        Serial.println("Could not start the DS3231 clock bus.");
    }
    lastClockRead = millis() - 1000;
#endif
}

void loop() {
    if (!audioReady) {
        delay(1000);
        return;
    }

    static ChimeEngine chimes(esp_random());
#if MUSICBOX_USE_RTC
    const uint32_t now = millis();
    if (clockBusReady && now - lastClockRead >= 1000) {
        lastClockRead = now;
        chimes.setPlaying(withinPlaybackHours());
    }
#else
    chimes.setPlaying(true);
#endif

    chimes.render(samples, framesPerBlock);
    for (std::size_t frame = 0; frame < framesPerBlock; ++frame) {
        stereo[2 * frame] = samples[frame];
        stereo[2 * frame + 1] = samples[frame];
    }
    if (audio.write(stereo, sizeof(stereo)) != sizeof(stereo)) {
        delay(5);
    }
}
