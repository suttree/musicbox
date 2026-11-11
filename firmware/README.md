# Ambient music box

The ESP32-S3 plays short digital-key phrases around the clock. Each phrase picks a new pentatonic scale, a tonic, a pace, and a melodic direction. The notes climb, descend, or wander, mostly one scale step at a time. Each phrase contains two to six notes and ends with a pause of 10 to 24 seconds before the next phrase starts.

Each note eases in over 48 milliseconds. The upper harmonics fade first, leaving a pair of close pitches that beat gently against each other. Note strength and decay vary, and up to six notes can ring together.

Each note leaves two soft echoes at 240 and 520 milliseconds, followed by quieter repeats. A long reverb fills the space between notes. About one phrase in four gets a little fuzz.

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
3. Open [WindChime.ino](WindChime/WindChime.ino) and upload. The first phrase starts at boot.

The wiring uses GPIO numbers from the [DevKitC-1 guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html). See the [MAX98357A breakout pinout](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pinouts) for power, speaker, and gain details.

## Adjust the sound

In [ChimeEngine.cpp](WindChime/ChimeEngine.cpp), lower `mixGain` for quieter playback. Change `phrasePace_` for more space between notes or `gapSeconds` for longer pauses between phrases. The `scales` table sets the available pitch patterns, and `voicePartials` controls the tone's brightness and decay.

Lower `fuzzMix` in the synth to soften the fuzz. In [ChimeEffects.cpp](WindChime/ChimeEffects.cpp), `echoMix` sets the level of the echoes, `echoFeedback` sets how much signal repeats, and `reverbMix` sets the level of the reverb.
