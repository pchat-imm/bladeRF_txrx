# transmit PSS seq from get_PSS_seq.py

# current work: read from this example to run buf that read from file
# https://github.com/Nuand/bladeRF/blob/master/host/examples/python/txrx/txrx.py


from bladerf import _bladerf
import numpy as np
import csv

# select input file
# input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/get_PSS_seq/PSS_NID2_0.csv'
# input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/get_PSS_seq/PSS_NID2_1.csv'
input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/get_PSS_seq/PSS_NID2_2.csv'

samples_list = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      IQ_PSS = row[0].strip()
      IQ_PSS = complex(IQ_PSS)
      samples_list.append(IQ_PSS)

samples = np.array(samples_list, dtype=np.complex64)
samples *= 32767.0 # scale so they can be stored as int16s (-32767 to 32767)
samples = samples.view(np.int16)
samples = samples.tobytes() # convert our samples to bytes and use them as transmit buffer

# Setup BladeRF
sdr = _bladerf.BladeRF()
tx_ch = sdr.Channel(_bladerf.CHANNEL_TX(0))

center_freq = 3.49e9
sample_rate = 15.36e6
gain = 0

tx_ch.frequency = center_freq
tx_ch.sample_rate = sample_rate
tx_ch.bandwidth = sample_rate/2
tx_ch.gain = gain

# Setup synchronous stream
# sync_tx can send up to ~4B samples
sdr.sync_config(layout= _bladerf.ChannelLayout.TX_X1,
                fmt = _bladerf.Format.SC16_Q11,
                num_buffers= 16,
                buffer_size= 8192,
                num_transfers=8,
                stream_timeout=3500)

print("Starting Transmit!")
tx_ch.enable = True

bytes_per_sample = 4
num_samples = len(samples) // bytes_per_sample
repeat = 2
num_repeat = 0

while True:
    if num_repeat != repeat: 
        sdr.sync_tx(samples, num_samples)   # write to bladeRF
        print("num_repeat: ", num_repeat)
        num_repeat += 1
    else:
        print("all transmitted")
        break

print("Transmit Complete!")
tx_ch.enable = False