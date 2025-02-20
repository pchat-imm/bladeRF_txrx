- serial bladerf board

```
Description:    Nuand bladeRF 2.0
Backend:        libusb
Serial:         04b118a874844193991adcd5af35ea4a
USB Bus:        4
USB Address:    3

Description:    Nuand bladeRF 2.0
Backend:        libusb
Serial:         6685e220048b4304b28eb62a5e1a5c78
USB Bus:        4
USB Address:    4
```

## example code
- example usage OAI with bladerf: https://gitlab.eurecom.fr/oai/openairinterface5g/-/blob/5b14f352817b21bf832fd9d161c0f7ab2428dbbe/radio/BLADERF/bladerf_lib.c
- sync tx_rx: https://github.com/Nuand/bladeRF/tree/624994d65c02ad414a01b29c84154260912f4e4f/host/examples/bladeRF-cli/sync_trx



## bladerf command
- call interactive interface of each bladeRF board by serial
```
bladeRF-cli -d "*:serial=6685e220048b4304b28eb62a5e1a5c78" -e"
> 

```