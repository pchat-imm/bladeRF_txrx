## bladeRF using python 
using Python binding and python API

from 
- PySDR Chap 7 BladeRF in Python https://pysdr.org/content/bladerf.html
- bladeRF example https://github.com/Nuand/bladeRF/blob/master/host/examples/python/txrx/txrx.py


1. setup python for bladeRF
```
cd bladeRF/host
cd ../libraries/libbladeRF_bindings/python
sudo python3 setup.py install
```
2. test python API
```
$ python3
>>> import bladerf
>>> bladerf.BladeRF()
<BladeRF(<DevInfo(libusb:device=4:2 instance=0 serial=04b118a874844193991adcd5af35ea4a)>)>
>>> exit()
```
3. write script
- print and set rx_ch
```
from bladerf import _bladerf
import numpy as np
import matplotlib.pyplot as plt

sdr = _bladerf.BladeRF()

## print basic sdr info
print("Device info:", _bladerf.get_device_list()[0])
print("Version: ", _bladerf.version())
print("Firmware version: ", sdr.get_fw_version())
print("FPGA version: ", sdr.get_fpga_version())

rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0))
print("sample_rate_range: ", rx_ch.sample_rate_range)
print("bandwidth_range: ", rx_ch.bandwidth_range)
print("frequency_range:", rx_ch.frequency_range)
print("gain_modes: ", rx_ch.gain_modes)
print("manual gain range:", sdr.get_gain_range(_bladerf.CHANNEL_RX(0)))

## example rx_ch setup
sample_rate = 15.36e6
center_freq = 3.5e9
gain = 50   # -15 to 60 dB
num_samples = int(1e6)

rx_ch.frequency = center_freq
rx_ch.sample_rate = sample_rate
rx_ch.bandwidth = sample_rate/2
rx_ch.gain_mode = _bladerf.GainMode.Manual
rx_ch.gain = gain
```
- setup synchronous stream and receive buffer. The while loop will continue to receive sample until the number of samples requested is reached. The received samples are stored in a separate numpy array. 
```

```
