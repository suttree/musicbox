#include "ChimeEffects.h"

namespace {
constexpr std::size_t shortEchoSamples = 7680; // 240 ms
constexpr float echoMix = 0.55f;
constexpr float echoFeedback = 0.45f;
constexpr float reverbMix = 0.52f;
}

float ChimeEffects::process(float input) {
    const float longEcho = echo_.oldest();
    const float shortEcho = echo_.tap(shortEchoSamples);
    const float echoInput = input + echoFeedback * longEcho;
    echoLowpass_ += 0.20f * (echoInput - echoLowpass_);
    echo_.push(echoLowpass_);
    const float echoes = echoMix * (0.45f * shortEcho + 0.55f * longEcho);

    // The staggered combs give the low frequencies about 5.5 seconds to decay 60 dB.
    const float reverbInput = input + 0.45f * echoes;
    const float reflections = 0.25f * (
        comb1_.process(reverbInput, 0.943f) +
        comb2_.process(reverbInput, 0.929f) +
        comb3_.process(reverbInput, 0.914f) +
        comb4_.process(reverbInput, 0.896f));
    const float early = diffuse(diffuser1_, reflections);
    const float reverb = diffuse(diffuser2_, early);

    return input + echoes + reverbMix * reverb;
}
