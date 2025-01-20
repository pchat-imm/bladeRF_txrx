from bladerf import _bladerf
import numpy as np

sdr = _bladerf.BladeRF()
rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))

sample_rate = 10e6
center_freq = 100e6
gain = 33
num_samples = int(1e6)

rx_ch.frequency = 100e6
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain_mode = _bladerf.GainMode.Manual
rx_ch.gain = gain

# set synchronous stream to recieve samples
sdr.sync_config(layout=_bladerf.ChannelLayout.RX_X1,
                fmt = _bladerf.Format.SC16_Q11,
                num_buffers    = 16,
                buffer_size    = 8192,
                num_transfers  = 8,
                stream_timeout = 3500)

# create recieve buffer
bytes_per_sample = 4
buf = bytearray(1024 * bytes_per_sample)

# enable module to recieve sample
rx_ch.enable = True

# Receieve loop
x = np.zeros(num_samples, dtype=np.complex64)
num_samples_read = 0
while True:
    if num_samples > 0 and num_samples_read == num_samples:
        break
    elif num_samples > 0:
        num = min(len(buf) // bytes_per_sample, num_samples - num_samples_read)
        sdr.sync_rx(buf, num)
        samples = np.frombuffer(buf, dtype=np.int16)
        samples = samples[0::2] + 1j * samples[1::2] 
        samples /= 2048.0
        x[num_samples_read:num_samples_read+num] = samples[0:num]
        num_samples_read += num

print("Stopping")
rx_ch.enable = False
print(x[0:10])      # look at first 10 IQ samples
# if max(x) close to 1 (0.999), you are overloading/saturate ADC, 
# we want 0.5 - 0.8, should reduce the gain, or the signal is distorted, look smear in freq domain
print(np.max(x))    

## Spectrogram/ Waterfall
fft_size = 1024
num_rows = num_samples // fft_size
spectrogram = np.zeros(num_rows, fft_size)
for i in range(num_rows):
    # fftshift - Shift the zero-frequency component to the center of the spectrum.
    # 10log10(abs(fftshift(fft))**2)
    spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)
# extent = [(center_freq + sample_rate/-2)/1e6, ,]


extent = [(center_freq + sample_rate/-2)/1e6, (center_freq + sample_rate/2)/1e6, len(x)/sample_rate, 0]