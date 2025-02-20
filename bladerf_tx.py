## Toturial: https://pysdr.org/content/bladerf.html

from bladerf import _bladerf
import numpy as np


def setup_transmitter(freq, sample_rate, bandwidth, gain_tx):
    "setup bladeRF transmitter"

    devices = _bladerf.get_device_list()
    sdr = _bladerf.BladeRF(devinfo=devices[0])
    sdr.enable_module(_bladerf.CHANNEL_TX(0), True)
    print("sdr serials: ", sdr.get_serial())

    # Configure TX channel
    tx_ch = sdr.Channel(_bladerf.CHANNEL_TX(0))
    tx_ch.frequency = freq
    tx_ch.sample_rate = sample_rate
    tx_ch.bandwidth = bandwidth
    tx_ch.gain = gain_tx

        # Set up synchronous stream configuration
    sdr.sync_config(
        layout=_bladerf.ChannelLayout.TX_X1,
        fmt=_bladerf.Format.SC16_Q11,
        num_buffers=16,
        buffer_size=8192,
        num_transfers=8,
        stream_timeout=3500
    )

    return sdr, tx_ch

def generate_tone(sample_rate, num_samples, f_tone):
    "Generate a simple tone in IQ samples to transmit."

    t = np.arange(num_samples) / sample_rate
    samples = np.exp(1j * 2 * np.pi * f_tone * t)  # Generate a tone
    samples = samples.astype(np.complex64)
    samples *= 32767.0  # scale so they can be stored as int16s (-32767 to 32767)
    samples = samples.view(np.int16)
    return samples.tobytes()  # Return the byte buffer


def transmit_tone(sdr, tx_ch, buf, num_samples, repeat):
    """
    Transmit the generated tone repeatedly.
    """
    repeat_remaining = repeat - 1
    tx_ch.enable = True
    print("Starting Transmit!")
    
    while repeat_remaining >= 0:
        sdr.sync_tx(buf, num_samples)  # Write to bladeRF
        print(f"Repeat remaining: {repeat_remaining}")
        if repeat_remaining > 0:
            repeat_remaining -= 1
        else:
            break

    print("Stopping Transmit")
    tx_ch.enable = False

def transmit_file(IQ_file):
    samples = np.fromfile(IQ_file, dtype=np.int16) 
    buf = samples.tobytes() # convert our samples to bytes and use them as transmit buffer
    tx_ch.enable = True
    print("Starting Transmit!")
    sdr.sync_tx(buf, len(samples))  # Write to bladeRF
    # segmentation fault




if __name__ == "__main__":
    center_freq = 3410e6
    sample_rate = 10e6
    bandwidth = sample_rate/2
    gain_tx = 0
    num_samples = int(1e6)

    # setup transmitter
    sdr, tx_ch = setup_transmitter(center_freq, sample_rate, bandwidth, gain_tx)

    # Generate IQ samples to transmit
    # buf = generate_tone(sample_rate, num_samples, f_tone=1e6)

    # repeat = 30 
    # transmit_tone(sdr, tx_ch, buf, num_samples, repeat)

    IQ_file = 'waveform_IQComplex_fllay.csv'
    transmit_file(IQ_file)