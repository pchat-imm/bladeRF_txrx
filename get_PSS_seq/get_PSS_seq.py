import numpy as np
import scipy
import csv
import matplotlib.pyplot as plt
import py3gpp
# !python3 -m pip install py3gpp
from py3gpp import *

sampleRate = 15.36e6                            # samples per second
# fPhaseComp = 3.48384e+09
# minChannelBW = 10
# BlockPattern = "Case C"
# L_max = 8

nrbSSB = 20
mu = 1
scs = 15 * 2**mu
carrier = nrCarrierConfig(NSizeGrid = nrbSSB, SubcarrierSpacing = scs)

rxSampleRate = sampleRate
kPSS = np.arange((119-63), (119+64))    # np.arange(56, 183) # check on 3GPP standard 

# With downsampling
syncNfft = 256                  # minimum FFT Size to cover SS burst
syncSR = syncNfft * scs * 1e3

# loop PSS sequence
NID2 = 0
slotGrid = nrResourceGrid(carrier)
slotGrid  = slotGrid[:,0] 
slotGrid[kPSS] = nrPSS(NID2)

nSlot = 0
[refWaveform, info] = nrOFDMModulate(carrier=carrier, grid=slotGrid, scs=scs, initialNSlot=nSlot, SampleRate=syncSR, Nfft=syncNfft)     # mod w/ downsample sample rate
refWaveform = refWaveform[info['CyclicPrefixLengths'][0]:]; # remove CP

np.savetxt('get_PSS_seq/PSS_NID2_0.csv', refWaveform, delimiter=',')