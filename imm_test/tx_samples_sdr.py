## Toturial: https://pysdr.org/content/bladerf.html

from bladerf import _bladerf
import numpy as np

sdr = _bladerf.BladeRF()
tx_ch = sdr.Channel(_bladerf.CHANNEL_TX(0))

# tramsmit a simple tone
sample_rate = 10e6
center_freq = 100e6
gain = 0    # -15 to 60 dB, start low and slowly increase, and make sure antenna is connected
num_samples = int(1e6)
repeat = 30         # number of times to repeat our signal
print('duration of tranmission: ', num_samples/sample_rate*repeat, ' seconds')

## in case want to trasnsmit a sample from a file 
# samples = np.fromfile('yourfile.iq', dtype=np.int16) 
# buf = samples.tobytes() # convert our samples to bytes and use them as transmit buffer


## Generate IQ samples to tranmist
t = np.arange(num_samples)/sample_rate
f_tone = 1e6
samples = np.exp(1j*2*np.pi*f_tone*t)   # will be -1 or 1
samples = samples.astype(np.complex64)
samples *= 32767.0  # scale so they can be stored as int16s (-32767 to 32767)
samples = samples.view(np.int16)
buf = samples.tobytes() # convert our samples to bytes and use them as transmit buffer

tx_ch.frequency = center_freq
tx_ch.sample_rate = sample_rate
tx_ch.bandwidth = sample_rate/2
tx_ch.gain = gain

# Setup synchronous stream
# sync_tx can send up to ~4B samples
# send simple tones repeat 30 times
sdr.sync_config(layout= _bladerf.ChannelLayout.TX_X1,
                fmt = _bladerf.Format.SC16_Q11,
                num_buffers= 16,
                buffer_size= 8192,
                num_transfers=8,
                stream_timeout=3500)

print("Starting Transmit!")
repeat_remaining = repeat - 1
tx_ch.enable = True
while True:
    sdr.sync_tx(buf, num_samples)   # write to bladeRF
    print(repeat_remaining)
    if repeat_remaining > 0:
        repeat_remaining -= 1
    else:
        break

print("Stopping Transmit")
tx_ch.enable = False
