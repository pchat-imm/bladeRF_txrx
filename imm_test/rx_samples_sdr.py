from bladerf import _bladerf
import numpy as np
import matplotlib.pyplot as plt

sdr = _bladerf.BladeRF()

# print("Device info:", _bladerf.get_device_list()[0])
# print("Version: ", _bladerf.version())
# print("Firmware version: ", sdr.get_fw_version())
# print("FPGA version: ", sdr.get_fpga_version())

rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))     # 0 = first receive channel
# print("sample_rate_range: ", rx_ch.sample_rate_range)
# print("bandwidth_range: ", rx_ch.bandwidth_range)
# print("frequency_range:", rx_ch.frequency_range)
# print("gain_modes: ", rx_ch.gain_modes)
# print("manual gain range:", sdr.get_gain_range(_bladerf.CHANNEL_RX(0)))

sample_rate = 10e6
center_freq = 100e6
gain = 35   # -15 to 60 dB
num_samples = int(1e6)

rx_ch.frequency = center_freq
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain_mode = _bladerf.GainMode.Manual
rx_ch.gain = gain

##################################################
# Receiving samples in python 

# Setup synchronous stream
# config the device's RX for use with the sync interface
# SC16Q11 samples *with* metadata
sdr.sync_config(layout=_bladerf.ChannelLayout.RX_X1,   # Rx port 1 or port 2
                fmt = _bladerf.Format.SC16_Q11,        # init16s
                num_buffers    = 16,
                buffer_size    = 8192,
                num_transfers  = 8,
                stream_timeout = 3500)

# create recieve buffer
bytes_per_sample = 4    # SC16Q11 use 4 bytes per sample
buf = bytearray(1024 * bytes_per_sample)

# enable module
# remember to enable the frontend module before calling sync_rx() or it showed timeouts or other errors
print("Starting recieve")
rx_ch.enable = True

## Receive loop
# loop: num_samples_read until num_samples (1e6) is reached
# elif: Limited by either buffer size or remaining samples needed
x = np.zeros(num_samples, dtype=np.complex64)
num_samples_read = 0
while True:
    if num_samples > 0 and num_samples_read == num_samples:
        break
    elif num_samples > 0:
        num = min(len(buf) // bytes_per_sample, num_samples - num_samples_read)
    else:  # case num_samples = 0
        num = len(buf) // bytes_per_sample
    # receive IQ samples, read raw data from ADC of SDR for number of samples (num) into the buffer (buf)
    sdr.sync_rx(buf, num)   # Read into buffer  
    # Converts buffer to 16-bit integers(2 bytes per samples len(samples) = len(buf)/2)
    samples = np.frombuffer(buf, dtype=np.int16)    
    # convert to complex type, even part as real, odd part as imaginary (*j)
    samples = samples[0::2] + 1j * samples[1::2]     
    samples /= 2048.0   # scale to -1 to 1 (its using 12 bit ADC, 2^12 = 4096 => +-2048)
    x[num_samples_read:num_samples_read+num] = samples[0:num]   # store buf in samples array
    num_samples_read += num    # increment num_samples_read by num, by 1024 samples

print("Stopping")
rx_ch.enable = False
print(x[0:10])      # look at first 10 IQ samples
# if max(x) close to 1 (0.999), you are overloading/saturate ADC, 
# we want 0.5 - 0.8, should reduce the gain, or the signal is distorted, look smear in freq domain
print(np.max(x))   

## Spectrogram
fft_size = 2048
num_rows = len(x) // fft_size
spectrogram = np.zeros((num_rows, fft_size))

for i in range(num_rows):
    spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(x[i*fft_size:(i+1)*fft_size])))**2)
# extent = [95.0, 105.0, 0.1, 0]    
extent = [(center_freq + sample_rate/-2)/1e6, (center_freq + sample_rate/2)/1e6, len(x)/sample_rate, 0]

plt.imshow(spectrogram, aspect='auto', extent=extent)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Time (s)')
plt.show()


