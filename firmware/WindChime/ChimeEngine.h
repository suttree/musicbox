#pragma once

#include "ChimeEffects.h"

#include <cstddef>
#include <cstdint>

class ChimeEngine {
public:
    static constexpr uint32_t sampleRate = ChimeEffects::sampleRate;

    explicit ChimeEngine(uint32_t seed);
    void render(int16_t* samples, std::size_t count);

private:
    static constexpr int voiceCount = 6;
    static constexpr int partialCount = 4;

    struct Partial {
        float real;
        float imaginary;
        float rotationReal;
        float rotationImaginary;
    };

    struct Voice {
        Partial partials[partialCount]{};
        uint32_t duration = 0;
        uint32_t remaining = 0;
        bool fuzz = false;
    };

    uint32_t nextRandom();
    float uniform();
    void beginPhrase();
    void strike();

    Voice voices_[voiceCount]{};
    uint32_t randomState_;
    uint32_t samplesUntilStrike_ = 0;
    int strikesLeft_ = 0;
    int scaleIndex_;
    int degree_ = 0;
    int melodyDirection_ = 0;
    float tonicHz_ = 0.0f;
    float phrasePace_ = 0.0f;
    float phraseBrightness_ = 0.0f;
    bool phraseFuzz_ = false;
    ChimeEffects effects_;
};
