import numpy as np
import scipy
import csv
import matplotlib.pyplot as plt

from py3gpp import *

## download input_file
input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/based_IQ_find_NID2/waveform_IQComplex_fllay.csv'

waveform = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      IQComplex = row[0].strip()
      IQComplex = IQComplex.replace('i','j')
      IQComplex = complex(IQComplex)
      waveform.append(IQComplex)

# input
sampleRate = 15.36e6
nrbSSB = 20
mu = 1
scs = 15 * 2**mu
carrier = nrCarrierConfig(NSizeGrid = nrbSSB, SubcarrierSpacing = scs)
rxOfdmInfo = nrOFDMInfo(carrier)
Nfft = rxOfdmInfo['Nfft']                       # number of FFT samples
