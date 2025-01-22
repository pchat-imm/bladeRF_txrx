from bladerf import _bladerf
import numpy as np
import csv

# Setup BladeRF
sdr = _bladerf.BladeRF()

# Configure both TX and RX channels
tx_ch = sdr.Channel(_bladerf.CHANNEL_TX(0))
rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))

# Configure parameters for both channels
center_freq = 3.49e9
sample_rate = 15.36e6
gain = 0

# TX channel setup
tx_ch.frequency = center_freq
tx_ch.sample_rate = sample_rate
tx_ch.bandwidth = sample_rate/2
tx_ch.gain = gain

# RX channel setup
rx_ch.frequency = center_freq
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain = gain

# Read TX samples
input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/get_PSS_seq/PSS_NID2_0.csv'
samples_list = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        IQ_PSS = row[0].strip()
        IQ_PSS = complex(IQ_PSS)
        samples_list.append(IQ_PSS)

tx_samples = np.array(samples_list, dtype=np.complex64)
tx_samples *= 32767.0
tx_samples = tx_samples.view(np.int16)
tx_samples = tx_samples.tobytes()

# Setup RX buffer
bytes_per_sample = 4
buf_size = 8192
rx_buffer = bytearray(buf_size * bytes_per_sample)

# First configure and enable RX
sdr.sync_config(
    layout=_bladerf.ChannelLayout.RX_X1,
    fmt=_bladerf.Format.SC16_Q11,
    num_buffers=16,
    buffer_size=8192,
    num_transfers=8,
    stream_timeout=3500
)
rx_ch.enable = True

# Then configure and enable TX
sdr.sync_config(
    layout=_bladerf.ChannelLayout.TX_X1,
    fmt=_bladerf.Format.SC16_Q11,
    num_buffers=16,
    buffer_size=8192,
    num_transfers=8,
    stream_timeout=3500
)
tx_ch.enable = True

print("Starting TX and RX!")

num_tx_samples = len(tx_samples) // bytes_per_sample
num_rx_samples = len(rx_buffer) // bytes_per_sample

try:
    while True:
        # Start RX first
        sdr.sync_rx(rx_buffer, num_rx_samples)
        
        # Then do TX
        sdr.sync_tx(tx_samples, num_tx_samples)
        
        # Process received samples
        rx_data = np.frombuffer(rx_buffer, dtype=np.int16).view(np.complex64)
        rx_data = rx_data / 32767.0
        
        print(f"TX samples: {num_tx_samples}, RX samples: {num_rx_samples}")

        break
        
# except KeyboardInterrupt:
#     print("\nStopping TX and RX...")
finally:
    rx_ch.enable = False
    tx_ch.enable = False
    sdr.close()