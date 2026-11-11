# Wind chime music box

This sketch makes its own audio on an ESP32-S3. Each strike picks a tube from a D major pentatonic scale and starts four damped sine waves. The higher resonances die away first. The box plays two to five strikes per gust, 1.3 to 3.8 seconds apart, then waits 7 to 16 seconds. It mixes up to six ringing notes at a time.

The sketch sends 32 kHz, 16-bit audio directly to an I²S amp. The bench setup runs offline from USB power.

## Bench setup

Use an ESP32-S3-DevKitC-1, a MAX98357A breakout, and an 8 Ω passive speaker rated for at least 2 W. Power the DevKitC by USB and connect the amp as follows.

| MAX98357A | Connection |
| --- | --- |
| VIN | DevKitC 5V |
| GND | DevKitC GND |
| BCLK | GPIO 4 |
| LRC or LRCLK | GPIO 5 |
| DIN | GPIO 6 |
| Speaker + and − | The two speaker terminals |

The amp drives both speaker terminals. Keep both speaker wires off ground. Use a USB supply and cable that can power the board and amp together. Check the breakout's pinout before wiring it.

1. In Arduino IDE, add the [Espressif Boards Manager URL](https://espressif.github.io/arduino-esp32/package_esp32_index.json) to **Additional boards manager URLs**.
2. Install **esp32 by Espressif Systems** version 3.x in Boards Manager. Select **ESP32S3 Dev Module** and the board's serial port.
3. Open [WindChime.ino](WindChime/WindChime.ino) and upload. The first strike starts at boot, followed by short groups of notes and pauses.

The wiring uses GPIO numbers from the [DevKitC-1 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html). See the [MAX98357A breakout pinout](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts) for power, speaker, and gain details.

## Optional hours

The default sketch plays continuously. To use the old Musicbox windows, connect a battery-backed DS3231 breakout with 3.3 V I²C pull-ups. Use GPIO 8 for SDA, GPIO 9 for SCL, and common ground. Use a breakout rated to run at 3.3 V and power it from 3V3.

Install Adafruit RTClib and its dependencies in Library Manager. Open the [RTClib DS3231 example](https://github.com/adafruit/RTClib/blob/master/examples/ds3231/ds3231.ino) and add `Wire.setPins(8, 9)` before `rtc.begin()`. The example sets an unset clock to the sketch's compile time in 24-hour mode. To reset a running clock, enable the example's unconditional `rtc.adjust()` call. Check the time it prints before uploading WindChime again. Adjust the clock when local clocks change.

Set `MUSICBOX_USE_RTC` to `1` in the sketch and upload. The box starts new strikes between 06:00 and 09:00, between 18:00 and 23:00, and between 12:00 and 14:00 on weekends. Ringing notes decay when a window closes or the clock becomes unavailable.

## Adjust the sound

In [ChimeEngine.cpp](WindChime/ChimeEngine.cpp), lower `mixGain` for quieter playback. Change `gapSeconds` for more space between notes or `rootHz` to shift all tubes up or down together. The `resonances` table controls the brightness and ring time.
