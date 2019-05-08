import numpy as np
import wave
import time


def generate_samples(stop_time, signal_list, fs):
  # generate a sample array for every tone
  sample_array_list = []
  for s in signal_list:
    s_time = s[0]
    s_freq = s[1]
    s_duration = s[2]
    prefix = np.zeros(s_time*int(fs/1000), dtype=np.float32)
    tone = 1.0/len(signal_list)*np.sin(2*np.pi*s_freq*np.arange(0., s_duration/1000, 1/fs), dtype=np.float32)
    suffix = np.zeros((stop_time-s_time-s_duration)*int(fs/1000), dtype=np.float32)
    sample_array_list.append(np.concatenate([prefix, tone, suffix]))
  samples = np.sum(sample_array_list, axis=0)
  #samples = np.multiply(1/np.amax(samples), samples, dtype=np.float32)
  return samples

def write_wav(f_name, samples, fs):
  wav_file = wave.open(f_name, 'wb')
  wav_file.setnchannels(1)
  wav_file.setsampwidth(2)
  wav_file.setframerate(fs)
  wav_file.writeframes(np.int16(32767*samples))
  wav_file.close()


class VirtualSoundRecorder():
  def __init__(self, f_name='virtualsound.wav', fs=48000):
    self.f_name = f_name
    self.fs = fs
    self.signal_list = []
    self.start_time = None

  def start(self):
    start_time = int(time.time() * 1000)
    self.start_time = start_time

  def stop(self):
    #print(self.signal_list)
    stop_time = int(time.time() * 1000)-self.start_time
    self.stop_time = stop_time
    return [self.stop_time, self.signal_list]

  def record(self, freq, duration):
    self.signal_list.append((int(time.time() * 1000)-self.start_time, freq, duration))


if __name__ == "__main__":
  usr = input('0 to check VSR, 1 to check generate_samples: ').strip('\n').strip()
  if usr == '0':
    vsr = VirtualSoundRecorder()
    vsr.start()
    time.sleep(1)
    vsr.record(440, 1000)
    time.sleep(2)
    vsr.record(460, 1000)
    vsr.record(480, 1000)
    time.sleep(2)
    vsr.record(600, 1000)
    time.sleep(2)
    vsr.stop()
  elif usr == '1':
    samples = generate_samples(7000, [(4394, 460, 1000), (4396, 1000, 1000), (4398, 1540, 1000)], 48000)
    #samples = generate_samples(3000, [(1200, 460, 1000)], 48000)
    #samples = generate_samples(3000, [(1200, 460, 1000), (1200, 600, 1000)], 48000)
    write_wav('virtualsound.wav', samples, 48000)
