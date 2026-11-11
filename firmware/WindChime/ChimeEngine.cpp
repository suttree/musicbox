#include "ChimeEngine.h"

#include <algorithm>
#include <cmath>

namespace {
constexpr float twoPi = 6.28318530718f;
constexpr float lowestTonicHz = 195.9977f; // G3
constexpr uint32_t attackSamples = ChimeEngine::sampleRate * 48 / 1000;
constexpr uint32_t releaseSamples = ChimeEngine::sampleRate / 2;
constexpr float mixGain = 0.65f;
constexpr float fuzzMix = 0.38f;

constexpr int degreesPerOctave = 5;
constexpr int highestDegree = 7;
constexpr int scales[][degreesPerOctave] = {
    {0, 2, 4, 7, 9},  // Major pentatonic
    {0, 3, 5, 7, 10}, // Minor pentatonic
    {0, 2, 5, 7, 10}, // Suspended pentatonic
    {0, 3, 5, 8, 10}, // Man Gong
};
constexpr int scaleCount = sizeof(scales) / sizeof(scales[0]);

struct PartialTuning {
    float ratio;
    float level;
    float decaySeconds;
};

constexpr PartialTuning voicePartials[] = {
    {1.0f, 0.68f, 1.80f},
    {1.003f, 0.15f, 1.25f}, // A slightly detuned copy of the fundamental.
    {2.0f, 0.19f, 0.67f},
    {3.0f, 0.075f, 0.26f},
};
}

ChimeEngine::ChimeEngine(uint32_t seed)
    : randomState_(seed == 0 ? 1 : seed), scaleIndex_(nextRandom() % scaleCount) {}

uint32_t ChimeEngine::nextRandom() {
    randomState_ ^= randomState_ << 13;
    randomState_ ^= randomState_ >> 17;
    randomState_ ^= randomState_ << 5;
    return randomState_;
}

float ChimeEngine::uniform() {
    return static_cast<float>(nextRandom() >> 8) / 16777216.0f;
}

void ChimeEngine::beginPhrase() {
    scaleIndex_ = (scaleIndex_ + 1 + nextRandom() % (scaleCount - 1)) % scaleCount;
    tonicHz_ = lowestTonicHz * std::exp2((nextRandom() % 8) / 12.0f);
    strikesLeft_ = 2 + nextRandom() % 5;
    degree_ = 1 + nextRandom() % 5;
    melodyDirection_ = static_cast<int>(nextRandom() % 3) - 1;
    phrasePace_ = 1.4f + uniform() * 1.7f;
    phraseBrightness_ = 0.55f + uniform() * 0.55f;
    phraseFuzz_ = nextRandom() % 4 == 0;
}

void ChimeEngine::strike() {
    if (strikesLeft_ == 0) {
        beginPhrase();
    }
    --strikesLeft_;
    const float gapSeconds = strikesLeft_ == 0
        ? 10.0f + uniform() * 14.0f
        : phrasePace_ * (0.7f + uniform() * 0.65f);
    samplesUntilStrike_ = static_cast<uint32_t>(gapSeconds * sampleRate);

    const int semitones = scales[scaleIndex_][degree_ % degreesPerOctave]
        + 12 * (degree_ / degreesPerOctave);
    const float frequency = tonicHz_ * std::exp2(semitones / 12.0f);

    // Move mostly by scale steps. A climb or descent turns at the edge of the range.
    const int direction = melodyDirection_ == 0
        ? (nextRandom() % 2 == 0 ? -1 : 1)
        : melodyDirection_;
    const int step = direction * (nextRandom() % 4 == 0 ? 2 : 1);
    const int nextDegree = degree_ + step;
    if (nextDegree < 0 || nextDegree > highestDegree) {
        degree_ -= step;
        melodyDirection_ = -melodyDirection_;
    } else {
        degree_ = nextDegree;
    }

    for (auto& voice : voices_) {
        if (voice.remaining != 0) {
            continue;
        }

        const float strength = 0.13f + uniform() * 0.18f;
        const float decayScale = 0.58f + uniform() * 0.80f;

        for (int i = 0; i < partialCount; ++i) {
            const auto& tuning = voicePartials[i];
            const float angle = twoPi * frequency * tuning.ratio / sampleRate;
            const float decay = std::exp(-1.0f / (sampleRate * tuning.decaySeconds * decayScale));
            const float brightness = tuning.ratio >= 2.0f ? phraseBrightness_ : 1.0f;
            voice.partials[i] = {
                strength * tuning.level * brightness,
                0.0f,
                decay * std::cos(angle),
                decay * std::sin(angle),
            };
        }
        voice.duration = static_cast<uint32_t>(8.5f * decayScale * sampleRate);
        voice.remaining = voice.duration;
        voice.fuzz = phraseFuzz_;
        return;
    }
}

void ChimeEngine::render(int16_t* samples, std::size_t count) {
    for (std::size_t frame = 0; frame < count; ++frame) {
        if (samplesUntilStrike_ == 0) {
            strike();
        }
        --samplesUntilStrike_;

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

            if (voice.fuzz) {
                const float driven = std::clamp(8.0f * sum, -1.0f, 1.0f);
                const float softened = 0.25f * (driven - driven * driven * driven / 3.0f);
                sum += fuzzMix * (softened - sum);
            }

            const uint32_t age = voice.duration - voice.remaining;
            if (age < attackSamples) {
                const float attack = static_cast<float>(age) / attackSamples;
                sum *= attack * attack * (3.0f - 2.0f * attack);
            } else if (voice.remaining <= releaseSamples) {
                sum *= static_cast<float>(voice.remaining - 1) / releaseSamples;
            }
            mix += sum;
            --voice.remaining;
        }

        const float scaled = mixGain * effects_.process(mix);
        const float limited = std::clamp(scaled, -1.0f, 1.0f);
        samples[frame] = static_cast<int16_t>(limited * 32767.0f);
    }
}
