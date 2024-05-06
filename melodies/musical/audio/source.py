import math
import numpy
import numpy as np

def silence(length, rate=44100):
    ''' Generate 'length' seconds of silence at 'rate'
    '''
    return numpy.zeros(int(length * rate))


def pygamesound(sound):
    ''' Create numpy array from pygame sound object
        rate is determined by pygame.mixer settings
    '''
    import pygame
    pygame.sndarray.use_arraytype('numpy')
    array = pygame.sndarray.array(sound)
    rate, format, channels = pygame.mixer.get_init()
    data = numpy.zeros(len(array))
    for i, sample in enumerate(array):
        data[i] = sum(sample)
    if format < 0:
        data /= (2 ** -format) / 2
    else:
        data = (data / (2 ** format)) * 2 - 1
    return data


def generate_wave_input(freq, length, rate=44100, phase=0.0):
    ''' Used by waveform generators to create frequency-scaled input array

        Courtesy of threepineapples:
          https://code.google.com/p/python-musical/issues/detail?id=2
    '''
    length = int(length * rate)
    t = numpy.arange(length) / float(rate)
    omega = float(freq) * 2 * math.pi
    phase *= 2 * math.pi  
    return omega * t + phase


def sine(freq, length, rate=44100, phase=0.0):
    ''' Generate sine wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return numpy.sin(data)


def _sawtooth(t):
    ''' Generate sawtooth wave from wave input array.
    '''
    tmod = numpy.mod(t, 2 * numpy.pi)
    return (tmod / numpy.pi) - 1


def sawtooth(freq, length, rate=44100, phase=0.0):
    ''' Generate sawtooth wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return _sawtooth(data)


def _square(t, duty=0.5):
    ''' Generate square wave from wave input array with specific 'duty'.
    '''
    y = numpy.zeros(t.shape)
    tmod = numpy.mod(t, 2 * numpy.pi)
    mask = tmod < duty * 2 * numpy.pi
    numpy.place(y, mask, 1)
    numpy.place(y, (1 - mask), -1)
    return y


def square(freq, length, rate=44100, phase=0.0):
    ''' Generate square wave for frequency of 'length' seconds long
        at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
        into the wave that it starts on.
    '''
    data = generate_wave_input(freq, length, rate, phase)
    return _square(data)

ringbuffer_cache = {}
def ringbuffer(data, length, decay=1.0, rate=44100):
    ''' Repeat data for 'length' amount of time, smoothing to reduce higher
        frequency oscillation. decay is the percent of amplitude decrease.
    '''
    key = (hash(f"{data}-{length}-{decay}-{rate}"))
    if key not in ringbuffer_cache:
        phase = len(data)
        length = int(rate * length)
        out = numpy.resize(data, length)
        for i in range(phase, length):
            index = i - phase
            out[i] = (out[index] + out[index + 1]) * 0.5 * decay
            ringbuffer_cache[key] = out
    #return out
    return ringbuffer_cache[key]

def pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 2 - 1 # original
    #data = numpy.random.random(phase) * 0.8 - 0.4 # softer
    #data = numpy.sin(numpy.linspace(0, numpy.pi * 2, phase)) # electronic
    #decay = 1.0 # greater sustain
    return ringbuffer(data, length, decay, rate) # original
    #reverb_length = 2.0  # Adjust the reverb length as desired # more ambient
    #reverb_decay = 0.5  # Adjust the reverb decay as desired
    #return ringbuffer(data, length + reverb_length, decay * reverb_decay, rate)

def soft_pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 0.8 - 0.4 # softer
    return ringbuffer(data, length, decay, rate) # original
    
def soft_ambient_pluck(freq, length, decay=0.999, rate=44100):
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 0.8 - 0.4
    sound = ringbuffer(data, length, decay, rate)
    reverb_length = 2.0
    reverb_decay = 0.5
    return ringbuffer(sound, length + reverb_length, decay * reverb_decay, rate)

def electronic_pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.sin(numpy.linspace(0, numpy.pi * 2, phase))
    return ringbuffer(data, length, decay, rate)
    
def sustained_pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 2 - 1
    decay = 0.999 # greater sustain
    return ringbuffer(data, length, decay, rate) # original

def ambient_pluck(freq, length, decay=0.998, rate=44100):
    ''' Create a pluck noise at freq by sending white noise through a ring buffer
        http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
    '''
    freq = float(freq)
    phase = int(rate / freq)
    data = numpy.random.random(phase) * 2 - 1
    reverb_length = 2.0  # Adjust the reverb length as desired # more ambient
    reverb_decay = 0.5  # Adjust the reverb decay as desired
    return ringbuffer(data, length + reverb_length, decay * reverb_decay, rate)
    
import numpy as np

def sine_wave(freq, length, rate=44100):
    t = np.linspace(0, length, int(length * rate), endpoint=False)
    data = np.sin(2 * np.pi * freq * t)
    return data

def solfeggio_pluck(freq, length, decay=0.998, rate=44100):
    solfeggio_freqs = [396, 417, 528, 639, 741, 852, 963]  # Solfeggio frequencies
    
    # Find the nearest solfeggio frequency to the given frequency
    nearest_freq = min(solfeggio_freqs, key=lambda x: abs(x - freq))
    
    # Generate a sine wave with the nearest solfeggio frequency
    data = sine_wave(nearest_freq, length, rate)
    
    # Apply a decay envelope
    envelope = np.exp(-np.linspace(0, length, int(length * rate)) * (1 - decay))
    data *= envelope
    
    return data

# Example usage
freq = 440  # Desired frequency
length = 2.0  # Length of the sound in seconds
decay = 0.995  # Decay factor for a more ambient sound

sound = solfeggio_pluck(freq, length, decay)