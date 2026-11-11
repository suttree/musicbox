#include "ChimeEngine.h"

#include <cmath>

namespace {
constexpr float twoPi = 6.28318530718f;
constexpr float rootHz = 293.6648f; // D4
constexpr uint32_t attackSamples = ChimeEngine::sampleRate * 8 / 1000;
constexpr uint32_t releaseSamples = ChimeEngine::sampleRate / 2;
constexpr uint32_t noteSamples = ChimeEngine::sampleRate * 12;
constexpr float mixGain = 0.65f;

// D major pentatonic. Repeated lower degrees keep the highest tubes occasional.
constexpr int tubes[] = {0, 0, 2, 4, 4, 7, 7, 9, 12, 14, 16, 19};
constexpr int tubeCount = sizeof(tubes) / sizeof(tubes[0]);

struct Resonance {
    float ratio;
    float level;
    float decaySeconds;
};

constexpr Resonance resonances[] = {
    {1.0f, 0.74f, 1.65f},
    {2.01f, 0.18f, 0.85f},
    {2.76f, 0.10f, 0.53f},
    {4.07f, 0.045f, 0.27f},
};
}

ChimeEngine::ChimeEngine(uint32_t seed)
    : randomState_(seed == 0 ? 1 : seed) {}

void ChimeEngine::setPlaying(bool playing) {
    if (playing && !playing_) {
        samplesUntilStrike_ = 0;
        strikesLeft_ = 0;
    }
    playing_ = playing;
}

uint32_t ChimeEngine::nextRandom() {
    randomState_ ^= randomState_ << 13;
    randomState_ ^= randomState_ >> 17;
    randomState_ ^= randomState_ << 5;
    return randomState_;
}

float ChimeEngine::uniform() {
    return static_cast<float>(nextRandom() >> 8) / 16777216.0f;
}

void ChimeEngine::strike() {
    if (strikesLeft_ == 0) {
        strikesLeft_ = 2 + nextRandom() % 4;
    }
    --strikesLeft_;
    const float gapSeconds = strikesLeft_ == 0
        ? 7.0f + uniform() * 9.0f
        : 1.3f + uniform() * 2.5f;
    samplesUntilStrike_ = static_cast<uint32_t>(gapSeconds * sampleRate);

    for (auto& voice : voices_) {
        if (voice.remaining != 0) {
            continue;
        }

        int tube = nextRandom() % tubeCount;
        // Skip the last pitch, including its duplicate entries in the table.
        while (lastTube_ >= 0 && tubes[tube] == tubes[lastTube_]) {
            tube = (tube + 1) % tubeCount;
        }
        lastTube_ = tube;
        const float frequency = rootHz * std::exp2(tubes[tube] / 12.0f);
        const float strength = 0.16f + uniform() * 0.17f;
        const float decayScale = 0.8f + uniform() * 0.35f;

        for (int i = 0; i < partialCount; ++i) {
            const auto& resonance = resonances[i];
            const float angle = twoPi * frequency * resonance.ratio / sampleRate;
            const float decay = std::exp(-1.0f / (sampleRate * resonance.decaySeconds * decayScale));
            voice.partials[i] = {
                strength * resonance.level,
                0.0f,
                decay * std::cos(angle),
                decay * std::sin(angle),
            };
        }
        voice.remaining = noteSamples;
        return;
    }
}

void ChimeEngine::render(int16_t* samples, std::size_t count) {
    for (std::size_t frame = 0; frame < count; ++frame) {
        if (playing_) {
            if (samplesUntilStrike_ == 0) {
                strike();
            }
            --samplesUntilStrike_;
        }

        float mix = 0.0f;
        for (auto& voice : voices_) {
            if (voice.remaining == 0) {
                continue;
            }

            float sum = 0.0f;
            for (auto& partial : voice.partials) {
                // One complex rotation advances the sine and damps it.
                const float real = partial.real * partial.rotationReal
                    - partial.imaginary * partial.rotationImaginary;
                partial.imaginary = partial.real * partial.rotationImaginary
                    + partial.imaginary * partial.rotationReal;
                partial.real = real;
                sum += partial.imaginary;
            }

            const uint32_t age = noteSamples - voice.remaining;
            if (age < attackSamples) {
                sum *= static_cast<float>(age) / attackSamples;
            } else if (voice.remaining <= releaseSamples) {
                sum *= static_cast<float>(voice.remaining - 1) / releaseSamples;
            }
            mix += sum;
            --voice.remaining;
        }

        const float scaled = mix * mixGain;
        const float limited = std::fmax(-1.0f, std::fmin(1.0f, scaled));
        samples[frame] = static_cast<int16_t>(limited * 32767.0f);
    }
}
