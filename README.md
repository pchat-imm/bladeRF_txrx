### current proposal
<img src = https://github.com/user-attachments/assets/dc222c18-7651-43be-85ac-65e08671c456 width=70%>

## current process 
at folder `bladeRF_txrx/based_IQ_find_NID2/trial`
- correct code of previous repo `iq_python` at `get_clean_CFO.py`
- **main**: want to correlate `wavefrom` of SDR with `refWaveform` from PSS_seq
    - the `waveform` need to be frequency shift and downsample first
    - so they will be 6 rxWaveformDS with 3 refWaveform

- `get_PSS_py.py` to get PSS_seq [0,1,2] and store in `/PSS_seq`
- `load_all_PSS_seq.py` to load PSS_seq from previous step, store as List in a Dictionary

## current tasks
- how to multithread all
- may read `cluade.ai` suggestion code 
- plan flow and paramaters of the system

## the planned proposal
**equipment** 
- 1 computer
- 1 sdr tx_srsRAN
- 1 sdr rx the tx_srsRAN

**process**
1. the 1st_sdr tx_srsRAN
2. the 2nd_sdr rx the tx_srsRAN
3. save rx_srsRAN as IQ waveform
4. operate in multithreading
- correlate rx_srsRAN with stored_seq (PSS_seq + freq_shift) * 18 times
- get 18 values of max_corr
5. compare max_corr
- get peak_val_stored_seq
- get peak_ind_stored_seq
6. translate result 
- peak_val_stored_seq into NID2, coarse_freq_offset
- peak_index_stored_seq into offset


## other tasks for `get_PSS_seq`
- how to know if the tx_seq is correct or not?
- how to use 4GHz probe of oscilloscope
