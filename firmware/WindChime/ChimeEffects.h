#pragma once

#include <cstddef>

class ChimeEffects {
public:
    // Delay lengths below are in samples at 32 kHz.
    static constexpr unsigned sampleRate = 32000;

    float process(float input);

private:
    template<std::size_t Size>
    struct DelayLine {
        float samples[Size]{};
        std::size_t position = 0;

        float oldest() const {
            return samples[position];
        }

        float tap(std::size_t delay) const {
            const std::size_t index = position + Size - delay;
            return samples[index < Size ? index : index - Size];
        }

        void push(float input) {
            samples[position] = input;
            if (++position == Size) {
                position = 0;
            }
        }
    };

    template<std::size_t Size>
    struct DampedComb {
        DelayLine<Size> delay;
        float lowpass = 0.0f;

        float process(float input, float feedback) {
            const float delayed = delay.oldest();
            lowpass += 0.35f * (delayed - lowpass);
            delay.push(input + feedback * lowpass);
            return delayed;
        }
    };

    template<std::size_t Size>
    static float diffuse(DelayLine<Size>& delay, float input) {
        constexpr float feedback = 0.57f;
        const float output = delay.oldest() - feedback * input;
        delay.push(input + feedback * output);
        return output;
    }

    DelayLine<16640> echo_; // 520 ms
    float echoLowpass_ = 0.0f;
    DampedComb<1499> comb1_;
    DampedComb<1867> comb2_;
    DampedComb<2281> comb3_;
    DampedComb<2801> comb4_;
    DelayLine<211> diffuser1_;
    DelayLine<373> diffuser2_;
};
