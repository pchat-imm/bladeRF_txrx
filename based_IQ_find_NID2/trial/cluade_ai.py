import numpy as np
from concurrent.futures import ThreadPoolExecutor
import scipy.signal
import csv
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

def load_waveform(input_file: str) -> List[complex]:
    """Load and process the received waveform from CSV file."""
    waveform = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            IQComplex = row[0].strip().replace('i', 'j')
            IQComplex = complex(IQComplex)
            waveform.append(IQComplex)
    return waveform

def frequency_shift_and_downsample(waveform: List[complex], 
                                 sample_rate: float,
                                 sync_sr: float,
                                 freq_offset: float) -> np.ndarray:
    """Apply frequency shift and downsample the waveform."""
    t = np.arange(len(waveform)) / sample_rate
    # Frequency correction
    rx_waveform_freq_corrected = np.array(waveform) * np.exp(-1j * 2 * np.pi * freq_offset * t)
    # Downsample
    rx_waveform_ds = scipy.signal.resample_poly(rx_waveform_freq_corrected, 
                                              int(sync_sr), 
                                              int(sample_rate))
    return rx_waveform_ds

def correlate_sequence(rx_waveform: np.ndarray, 
                      ref_waveform: np.ndarray) -> Tuple[float, int]:
    """
    Correlate received waveform with reference waveform.
    Returns correlation magnitude and position of maximum correlation.
    """
    correlation = np.correlate(rx_waveform, ref_waveform, mode='full')
    max_idx = np.argmax(np.abs(correlation))
    max_value = np.abs(correlation[max_idx])
    return max_value, max_idx

def parallel_correlation(rx_waveform: np.ndarray, 
                        ref_waveforms: Dict[str, List[complex]]) -> Dict[str, Tuple[float, int]]:
    """Process correlations in parallel using ThreadPoolExecutor."""
    results = {}
    
    with ThreadPoolExecutor() as executor:
        future_to_nid2 = {
            executor.submit(correlate_sequence, rx_waveform, np.array(ref_waveform)): nid2
            for nid2, ref_waveform in ref_waveforms.items()
        }
        
        for future in future_to_nid2:
            nid2 = future_to_nid2[future]
            try:
                max_value, max_idx = future.result()
                results[nid2] = (max_value, max_idx)
            except Exception as e:
                print(f"Error processing {nid2}: {e}")
    
    return results

def process_pss_detection(input_file: str,
                         ref_waveforms: Dict[str, List[complex]],
                         sample_rate: float = 15.36e6,
                         nrb_ssb: int = 20,
                         mu: int = 1,
                         freq_shifts: List[float] = None) -> Dict[str, List[Tuple[float, int]]]:
    """
    Main processing function for PSS detection.
    Returns correlation results for each frequency shift and NID2.
    """
    if freq_shifts is None:
        freq_shifts = [-15e3, 0, 15e3]
    
    # Load waveform
    waveform = load_waveform(input_file)
    
    # Calculate parameters
    scs = 15 * 2**mu
    sync_nfft = 256  # minimum FFT Size to cover SS burst
    sync_sr = sync_nfft * scs * 1e3
    
    # Process each frequency shift
    all_results = {}
    for f_shift in freq_shifts:
        # Frequency shift and downsample
        rx_waveform_ds = frequency_shift_and_downsample(waveform, sample_rate, sync_sr, f_shift)
        
        # Parallel correlation
        results = parallel_correlation(rx_waveform_ds, ref_waveforms)
        all_results[f"fshift_{f_shift}"] = results
    
    return all_results

def plot_correlation_results(all_results: Dict[str, Dict[str, Tuple[float, int]]]):
    """Plot correlation results for visual analysis."""
    fig, axes = plt.subplots(len(all_results), 1, figsize=(12, 4*len(all_results)))
    if len(all_results) == 1:
        axes = [axes]
    
    for idx, (fshift, results) in enumerate(all_results.items()):
        correlation_values = [value[0] for value in results.values()]
        nid2_labels = list(results.keys())
        
        axes[idx].bar(nid2_labels, correlation_values)
        axes[idx].set_title(f'Correlation Results for {fshift}')
        axes[idx].set_ylabel('Correlation Magnitude')
        axes[idx].set_xlabel('NID2')
        
    plt.tight_layout()
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Parameters
    input_file = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/based_IQ_find_NID2/waveform_IQComplex_fllay.csv'
    base_path = '/home/chatchamon/workarea/npn_5g/bladeRF_txrx/based_IQ_find_NID2/trial/PSS_seq'
    
    # Load reference waveforms
    NID2_val = [0, 1, 2]
    ref_waveforms = {}
    for NID2 in NID2_val:
        ref_waveforms[f'NID2_{NID2}'] = []
        with open(f'{base_path}/NID2_{NID2}.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                IQ_PSS = complex(row[0].strip())
                ref_waveforms[f'NID2_{NID2}'].append(IQ_PSS)
    
    # Process correlations
    results = process_pss_detection(input_file, ref_waveforms)
    
    # Plot results
    plot_correlation_results(results)
    
    # Print maximum correlation for each frequency shift
    for fshift, corr_results in results.items():
        max_nid2 = max(corr_results.items(), key=lambda x: x[1][0])
        print(f"\nFrequency shift {fshift}:")
        print(f"Maximum correlation at NID2: {max_nid2[0]}")
        print(f"Correlation value: {max_nid2[1][0]}")
        print(f"Position: {max_nid2[1][1]}")