## import requirement
import numpy as np
import scipy
import csv
import matplotlib.pyplot as plt
# !python3 -m pip install py3gpp
from py3gpp import *

## load rx_srsRAN
input_file = '/home/chatchamon/workarea/IQ_constellation/iq_python/input/fllay_092024/waveform_IQComplex_fllay.csv'
waveform = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      IQComplex = row[0].strip()
      IQComplex = IQComplex.replace('i','j')
      IQComplex = complex(IQComplex)
      waveform.append(IQComplex)

## initial parameter
sampleRate = 15.36e6
nrbSSB = 20
mu = 1
scs = 15 * 2**mu
carrier = nrCarrierConfig(NSizeGrid = nrbSSB, SubcarrierSpacing = scs)
rxOfdmInfo = nrOFDMInfo(carrier)
Nfft = rxOfdmInfo['Nfft']  

## find CFO (coarseFrequencyOffset)
searchBW = 6*scs
kPSS = np.arange((119-63), (119+64))    # np.arange(56, 183) # check on 3GPP standard 
fshifts = np.arange(-searchBW, searchBW+scs, scs)*1e3/2     # half subcarrier step
peak_value = np.zeros((len(fshifts),3))
peak_index = np.zeros((len(fshifts),3), 'int')
t = np.arange(len(waveform))/sampleRate

# With downsampling
syncNfft = 256                  # minimum FFT Size to cover SS burst
syncSR = syncNfft * scs * 1e3

for fIdx in np.arange(len(fshifts), dtype='int'):
    coarseFrequencyOffset = fshifts[fIdx]
    rxWaveformFreqCorrected = waveform * np.exp(-1j*2*np.pi*coarseFrequencyOffset*t)
    rxWaveformDS = scipy.signal.resample_poly(rxWaveformFreqCorrected, syncSR, sampleRate)              # same with matlab code

    for NID2 in np.arange(3, dtype='int'):
        slotGrid = nrResourceGrid(carrier)
        slotGrid  = slotGrid[:,0] 
        slotGrid[kPSS] = nrPSS(NID2)

        nSlot = 0
        [refWaveform, info] = nrOFDMModulate(carrier=carrier, grid=slotGrid, scs=scs, initialNSlot=nSlot, SampleRate=syncSR, Nfft=syncNfft)     # mod w/ downsample sample rate
        refWaveform = refWaveform[info['CyclicPrefixLengths'][0]:]; # remove CP
        
        temp = scipy.signal.correlate(rxWaveformDS, refWaveform,'valid') 
        peak_index[fIdx, NID2] = np.argmax(np.abs(temp))
        peak_value[fIdx, NID2] = np.abs(temp[peak_index[fIdx, NID2]])

select_fIdx, select_NID2 = np.where(peak_value == np.max(peak_value))
coarseFrequencyOffset = fshifts[select_fIdx]

print("max_corr", np.max(peak_value))
print("coarseFrequencyOffset", coarseFrequencyOffset, "NID2", NID2)

# apply coarseFrequencyCorrect, and downsample
rxWaveformFreqCorrected =  waveform * np.exp(-1j*2*np.pi*coarseFrequencyOffset*t)
rxWaveformDS = scipy.signal.resample_poly(rxWaveformFreqCorrected, syncSR, sampleRate)  

syncOfdmInfo_SymbolLengths = 278
offset = int(peak_index[select_fIdx, select_NID2] + syncOfdmInfo_SymbolLengths)
print("offset", offset)