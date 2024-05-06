class Looper:
    def __init__(self, loop_length, num_loops=1, fade_time=0.1, rate=44100):
        self.loop_length = loop_length
        self.num_loops = num_loops
        self.fade_time = fade_time
        self.rate = rate
        self.buffer = None
        self.loop_samples = int(loop_length * rate)
        self.fade_samples = int(fade_time * rate)

    def record(self, data):
        if len(data) >= self.loop_samples:
            self.buffer = data[:self.loop_samples]
        else:
            self.buffer = np.pad(data, (0, self.loop_samples - len(data)), 'constant')

    def play(self):
        if self.buffer is None:
            raise ValueError("No audio recorded in the looper.")

        output = np.zeros(self.loop_samples * self.num_loops)

        for i in range(self.num_loops):
            start = i * self.loop_samples
            end = start + self.loop_samples

            if i == 0:
                # First loop, fade in
                fade_in = np.linspace(0, 1, self.fade_samples)
                output[start:start + self.fade_samples] = self.buffer[:self.fade_samples] * fade_in
                output[start + self.fade_samples:end] = self.buffer[self.fade_samples:]
            elif i == self.num_loops - 1:
                # Last loop, fade out
                fade_out = np.linspace(1, 0, self.fade_samples)
                output[start:end - self.fade_samples] = self.buffer[:-self.fade_samples]
                output[end - self.fade_samples:end] = self.buffer[-self.fade_samples:] * fade_out
            else:
                # Middle loops
                output[start:end] = self.buffer

        return output

    def clear(self):
        self.buffer = None
        
        
"""
# Create a looper with a loop length of 2 seconds and 3 loops
looper = Looper(loop_length=2, num_loops=3)

# Record audio data into the looper
audio_data = ...  # Get your audio data here
looper.record(audio_data)

# Play the looped audio
looped_audio = looper.play()

# Clear the looper's buffer
looper.clear()
"""