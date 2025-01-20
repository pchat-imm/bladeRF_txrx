# transmit PSS seq from get_PSS_seq.py
import numpy as np
import csv

input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/get_PSS_seq/PSS_NID2_0.csv'

samples_list = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      IQ_PSS = row[0].strip()
      IQ_PSS = complex(IQ_PSS)
      samples_list.append(IQ_PSS)

samples = np.array(samples_list, dtype=np.complex64)
samples *= 32767.0 # scale so they can be stored as int16s (-32767 to 32767)
samples.view(np.int16)
buf = samples.tobytes() # convert our samples to bytes and use them as transmit buffer
