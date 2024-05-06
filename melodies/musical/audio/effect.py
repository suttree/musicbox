from . import source

import noise, time
from noise import pnoise2
import numpy as np

# TODO: More effects. Distortion, echo, delay, reverb, phaser, pitch shift?
# TODO: Better generalize chorus/flanger (they share a lot of code)

import numpy as np

def modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (no feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = np.clip(out[i] * dry + data[index] * wet, -1.0, 1.0)
    return out

def feedback_modulated_delay(data, modwave, dry, wet):
    ''' Use LFO "modwave" as a delay modulator (with feedback)
    '''
    out = data.copy()
    for i in range(len(data)):
        index = int(i - modwave[i])
        if index >= 0 and index < len(data):
            out[i] = np.clip(out[i] * dry + out[index] * wet, -1.0, 1.0)
    return out

def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
    ''' Chorus effect
        http://en.wikipedia.org/wiki/Chorus_effect
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
    return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
    ''' Flanger effect
        http://en.wikipedia.org/wiki/Flanging
    '''
    length = float(len(data)) / rate
    mil = float(rate) / 1000
    delay *= mil
    depth *= mil
    modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
    return feedback_modulated_delay(data, modwave, dry, wet)


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
    ''' Tremolo effect
        http://en.wikipedia.org/wiki/Tremolo
    '''
    length = float(len(data)) / rate
    modwave = (source.sine(freq, length) / 2 + 0.5)
    return (data * dry) + ((data * modwave) * wet)


def shimmer(data, scale=0.3147, rate=44100):
    length = float(len(data)) / rate
    now = time.time()
    perlin = pnoise2(now * scale, length * scale, octaves=5, persistence=0.75, lacunarity=2.2)
    return (data * perlin)

def shimmer_wobble(data, scale=0.3147, depth=0.5, freq=5.0, rate=44100):
    length = float(len(data)) / rate
    now = time.time()
    
    # Generate Perlin noise for brightness
    perlin_brightness = pnoise2(now * scale, length * scale, octaves=5, persistence=0.75, lacunarity=2.2)
    
    # Generate Perlin noise for wobbliness
    perlin_wobble = pnoise2((now + 1000) * scale, length * scale, octaves=3, persistence=0.5, lacunarity=1.5)
    
    # Apply brightness modulation
    brightness_mod = (perlin_brightness + 1) / 2  # Normalize to range [0, 1]
    brightness_mod = np.power(brightness_mod, 2)  # Increase the brightness
    data_bright = data * brightness_mod
    
    # Apply wobble modulation
    wobble_mod = (perlin_wobble + 1) / 2  # Normalize to range [0, 1]
    wobble_mod = wobble_mod * 2 - 1  # Scale to range [-1, 1]
    wobble_mod = np.sin(wobble_mod * freq * np.pi * 2)  # Apply sinusoidal wobble
    data_wobble = data_bright + (data_bright * wobble_mod * depth)
    
    return data_wobble

def reverb(data, delay=50, decay=0.5, wet=0.5, rate=44100):
    ''' Reverb effect
    '''
    out = data.copy()
    delay_samples = int(delay * rate / 1000)
    decay_samples = int(decay * rate)
    
    for i in range(delay_samples, len(data)):
        out[i] += out[i - delay_samples] * decay
    
    return (data * (1 - wet)) + (out * wet)

def pan(data, pan_amount=0.5):
    ''' Panning effect
    '''
    # Validate pan_amount to be in range [-1, 1]
    pan_amount = max(-1, min(pan_amount, 1))

    # Calculate left and right channel gains based on pan_amount
    left_gain = np.sqrt(0.5 - pan_amount / 2)
    right_gain = np.sqrt(0.5 + pan_amount / 2)

    # Apply panning
    left_channel = data * left_gain
    right_channel = data * right_gain

    # Stack left and right channels horizontally
    panned_audio = np.column_stack((left_channel, right_channel))

    return panned_audio
    
def simple_pan(data, pan_amount=0.5):
    ''' Simple Panning effect
    '''
    # Validate pan_amount to be in range [0, 1]
    pan_amount = max(0, min(pan_amount, 1))

    # Split the audio into left and right channels
    left_channel = data * (1 - pan_amount)
    right_channel = data * pan_amount

    # Stack left and right channels horizontally
    panned_audio = np.column_stack((left_channel, right_channel))

    return panned_audio

def simple_delay(data, delay_samples=1000, feedback=0.5, wet=0.5):
    ''' Simple Delay effect
    '''
    # Create an empty array to store delayed audio
    delayed_audio = np.zeros_like(data)

    # Apply delay effect
    for i in range(delay_samples, len(data)):
        delayed_audio[i] = data[i - delay_samples] + feedback * delayed_audio[i - delay_samples]

    # Mix original and delayed audio
    output_audio = (1 - wet) * data + wet * delayed_audio

    return output_audio

def distortion(data, gain=5.0, clip_level=0.8):
    ''' Distortion effect
    '''
    clipped_data = np.tanh(data * gain) * clip_level
    return clipped_data

def echo(data, delay=0.5, decay=0.5, wet=0.5, rate=44100):
    ''' Echo effect
    '''
    delay_samples = int(delay * rate)
    output_audio = np.zeros_like(data)
    
    for i in range(len(data)):
        output_audio[i] = data[i]
        if i >= delay_samples:
            output_audio[i] += decay * output_audio[i - delay_samples]
    
    return (data * (1 - wet)) + (output_audio * wet)
    
import soundfile as sf
import resampy
import numpy as np
def pitch_shift(data, semitones, sample_rate=44100):
    """
    Apply pitch shifting to the audio data.
    
    :param data: numpy array representing the audio data
    :param semitones: number of semitones to shift the pitch
    :param sample_rate: sample rate of the audio data (default: 44100 Hz)
    :return: pitch-shifted audio data
    """
    pitch_ratio = 2 ** (semitones / 12)

    # Write the audio data to a temporary file
    temp_file = 'temp_audio.wav'
    sf.write(temp_file, data, sample_rate)

    # Read the audio data from the temporary file
    shifted_data, _ = sf.read(temp_file)

    # Resample the audio data to apply pitch shifting
    shifted_data = resampy.resample(shifted_data, sample_rate, int(sample_rate / pitch_ratio))

    return shifted_data
    
import numpy as np
from scipy.signal import lfilter
def wah(data, freq=1000, q=10, gain=2, rate=44100):
    ''' Wah effect
    '''
    freq = np.clip(freq, 0, rate / 2)
    q = np.clip(q, 1, 100)
    gain = np.clip(gain, 1, 10)

    # Calculate filter coefficients
    w0 = 2 * np.pi * freq / rate
    alpha = np.sin(w0) / (2 * q)
    b0 = (1 - np.cos(w0)) / 2
    b1 = 1 - np.cos(w0)
    b2 = b0
    a0 = 1 + alpha
    a1 = -2 * np.cos(w0)
    a2 = 1 - alpha

    # Apply filter
    b = [b0 / a0, b1 / a0, b2 / a0]
    a = [1, a1 / a0, a2 / a0]
    output = lfilter(b, a, data)

    # Apply gain
    output *= gain

    return output

def autowah(data, freq_range=(500, 3000), rate=44100, lfo_freq=2, q=10, gain=2):
    ''' Autowah effect
    '''
    min_freq, max_freq = freq_range
    lfo = np.sin(2 * np.pi * lfo_freq * np.arange(len(data)) / rate)
    freq = min_freq + (max_freq - min_freq) * (lfo + 1) / 2

    output = np.zeros_like(data)
    for i in range(len(data)):
        output[i] = wah(data[i:i+1], freq=freq[i], q=q, gain=gain, rate=rate)

    return output