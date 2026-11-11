#include <Arduino.h>
#include <ESP_I2S.h>
#include <esp_random.h>

#include "ChimeEngine.h"

namespace {
constexpr int bitClockPin = 4;
constexpr int wordSelectPin = 5;
constexpr int audioDataPin = 6;
constexpr std::size_t framesPerBlock = 256;

I2SClass audio;
int16_t samples[framesPerBlock];
int16_t stereo[framesPerBlock * 2];
bool audioReady = false;
}

void setup() {
    Serial.begin(115200);
    audio.setPins(bitClockPin, wordSelectPin, audioDataPin);
    audioReady = audio.begin(I2S_MODE_STD, ChimeEngine::sampleRate,
                             I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO);
    if (!audioReady) {
        Serial.println("Could not start I2S audio.");
    }
}

void loop() {
    if (!audioReady) {
        delay(1000);
        return;
    }

    static ChimeEngine chimes(esp_random());
    chimes.render(samples, framesPerBlock);
    for (std::size_t frame = 0; frame < framesPerBlock; ++frame) {
        stereo[2 * frame] = samples[frame];
        stereo[2 * frame + 1] = samples[frame];
    }
    if (audio.write(stereo, sizeof(stereo)) != sizeof(stereo)) {
        delay(5);
    }
}
