## basic bladef command (bladeRF-cli and bladerf-tool)
tutorial from
- PySDR Chap 7 BladeRF in Python https://pysdr.org/content/bladerf.html
- bladeRF CLI Tips and Tricks https://github.com/Nuand/bladeRF/wiki/bladeRF-CLI-Tips-and-Tricks

### bladeRF-cli
is command-line interface tool provide direct control and config of the bladeRF device. It is used for device config, signal tx and rx, calibration, debug, and general management.
- enter interactive mode
```
bladeRF-cli -i
```
- set board freq, bandwidth, samplerate, agc (automatic gain control) and print all setup
```
bladeRF> set frequency rx 1572.42M
bladeRF> set samplerate rx 8M
bladeRF> set bandwidth rx 5M

# Automatic gain control is enabled by default, you can set it off and set gains manually
# bladeRF> set agc off
# bladeRF> set gain rx 60

# print to see all setup
bladeRF> print

  RX1 Bandwidth:   5000000 Hz (Range: [200000, 56000000])
  RX2 Bandwidth:   5000000 Hz (Range: [200000, 56000000])
  TX1 Bandwidth:  18000000 Hz (Range: [200000, 56000000])
  TX2 Bandwidth:  18000000 Hz (Range: [200000, 56000000])

  RX1 Frequency: 1572419998 Hz (Range: [70000000, 6000000000])
  RX2 Frequency: 1572419998 Hz (Range: [70000000, 6000000000])
  TX1 Frequency: 2400000000 Hz (Range: [47000000, 6000000000])
  TX2 Frequency: 2400000000 Hz (Range: [47000000, 6000000000])

  Tuning Mode: Host

  Bit Mode: 16 bit samples

  Feature:  Default enabled

  RX1 AGC: Enabled   
  RX2 AGC: Enabled   

  Clock reference: none
  Clock input:     Onboard VCTCXO
  Clock output:    Disabled

  RX1 RSSI: preamble = -81 dB, symbol = -70 dB
  RX2 RSSI: preamble = -77 dB, symbol = -70 dB

  Loopback mode: none

  RX mux: BASEBAND - Baseband samples

  RX FIR Filter: normal (default)
  TX FIR Filter: bypass (default)

  Gain RX1 overall:   60 dB (Range: [-15, 60])
              full:   71 dB (Range: [-4, 71])
  Gain RX2 overall:   60 dB (Range: [-15, 60])
              full:   71 dB (Range: [-4, 71])
  Gain TX1 overall:   56 dB (Range: [-23.75, 66])
               dsa:  -90 dB (Range: [-89.75, 0])
  Gain TX2 overall:   56 dB (Range: [-23.75, 66])
               dsa:  -90 dB (Range: [-89.75, 0])

  RX1 sample rate: 8000000 0/1 (Range: [520834, 61440000])
  RX2 sample rate: 8000000 0/1 (Range: [520834, 61440000])
  TX1 sample rate: 8000000 0/1 (Range: [520834, 61440000])
  TX2 sample rate: 8000000 0/1 (Range: [520834, 61440000])

  Bias Tee (RX1): off
  Bias Tee (RX2): off
  Bias Tee (TX1): off
  Bias Tee (TX2): off

  Current VCTCXO trim: 0x1c59
  Stored VCTCXO trim:  0x1c59

  Hardware status:
    RFIC status:
      Tuning Mode:  Host
      Temperature:  30.7 degrees C
      CTRL_OUT:     0xf8 (0x035=0x00, 0x036=0xff)
    Power source:   USB Bus
    Power monitor:  4.88 V, 0.55 A, 2.62 W
    RF routing:
      RX1: RFIC 0x0 (A_BAL  ) <= SW 0x0 (OPEN   )
      RX2: RFIC 0x0 (A_BAL  ) <= SW 0x0 (OPEN   )
      TX1: RFIC 0x0 (TXA    ) => SW 0x0 (OPEN   )
      TX2: RFIC 0x0 (TXA    ) => SW 0x0 (OPEN   )
```


### bladerf-tool
is for basic administrative tasks and general device management 
- install bladerf-tool
```
cd bladeRF/host
cd ../libraries/libbladeRF_bindings/python
sudo python3 setup.py install
```
- `bladerf-tool probe` to list all connected bladeRF devices and display a summary of their connection 
```
>> bladerf-tool probe
Device Information
    backend  libusb
    serial   04b118a874844193991adcd5af35ea4a
    usb_bus  4
    usb_addr 2
    instance 0
```
- `bladerf-tool info` info on firmware, FPGA, and hardware detailed
```
>> bladerf-tool info
*** Devices found: 1

*** Device 0
Board Name        bladerf2
Device Speed      Super
FPGA Size         49
FPGA Configured   True
FPGA Version      v0.12.0 ("0.12.0")
Flash Size        32 Mbit 
Firmware Version  v2.4.0 ("2.4.0-git-a3d5c55f")
RX Channel Count  2
  Channel RX1:
    Gain          60
    Gain Mode     SlowAttack_AGC
    Symbol RSSI   -52
    Frequency     2400000000
    Bandwidth     18000000
    Sample Rate   30720000
  Channel RX2:
    Gain          60
    Gain Mode     SlowAttack_AGC
    Symbol RSSI   -52
    Frequency     2400000000
    Bandwidth     18000000
    Sample Rate   30720000
TX Channel Count  2
  Channel TX1:
    Gain          56
    Frequency     2400000000
    Bandwidth     18000000
    Sample Rate   30720000
  Channel TX2:
    Gain          56
    Frequency     2400000000
    Bandwidth     18000000
    Sample Rate   30720000
```

### Receiving samples
1. receive samples using `bladeRF-cli`, of num_of_sample = 20M
- note that, when writing large number of samples, especially at higher sample rate, you should use the binary format to save on disk space, using `SC16_Q11` format
- note that binary SC16_Q11 format, 1 samples consumes 4 bytes of memory/disk space.
- we can save format as `bin (file=my_samples.sc16q11 format=bin)` or `csv (file=my_samples.csv format=csv)` 
```
bladeRF-cli -i
bladeRF> set frequency rx 1572.42M
bladeRF> set samplerate rx 8M
bladeRF> set bandwidth rx 5M
bladeRF>
bladeRF> rx config file=my_samples.sc16q11 format=bin n=20M
bladeRF> rx start
bladeRF> rx 

  State: Running
  Channels: RX1
  Last error: None
  File: my_samples.sc16q11
  File format: SC16 Q11, Binary
  # Samples: 20971520
  # Buffers: 32
  # Samples per buffer: 32768
  # Transfers: 16
  Timeout (ms): 1000

bladeRF> rx wait
bladeRF> rx

  State: Idle
  Channels: RX1
  Last error: None
  File: my_samples.sc16q11
  File format: SC16 Q11, Binary
  # Samples: 20971520
  # Buffers: 32
  # Samples per buffer: 32768
  # Transfers: 16
  Timeout (ms): 1000

```
2. receive samples using `bladerf-tool`
recieve 1M samples in the FM radio band, at 10 MHz sample rate to a file samples.sc16 at center_freq 100 MHz
```
 bladerf-tool rx --num-samples 10000000 samples.sc16 100e6 10e6
```