# task for `get_PSS_seq`
### 1. test using sdr to tx and keysight to rx
**expected result**: periodically spike 
**equipment**: 1 SDR, 1 Laptop, 1 Keysight
- try transmit the samples file from `tx_PSS_seq.py`
- use keysight waterfall to receive samples
- check if the recieve samples the same with the transmitted samples
- if not, change the transmitted file in `get_PSS_seq.py`

### 2. use probe 4 GHz
**equipment**: 1 SDR, 1 Laptop, 1 Oscilloscope

### 3. handle multiple SDR

**note**
- to interrupt running bladeRF just keyboard interrupt (type `Ctrl + C`)