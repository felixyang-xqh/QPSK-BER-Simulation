"""
QPSK BER Simulation
-------------------
This beginner-friendly script simulates a QPSK communication system.

Main steps:
1. Generate random bits
2. Map every 2 bits to one QPSK symbol
3. Add AWGN noise to simulate a noisy channel
4. Demodulate received symbols back to bits
5. Calculate BER under different SNR values
6. Plot the BER-SNR curve and a constellation diagram
"""

import numpy as np
import matplotlib.pyplot as plt


# Gray coding map:
# 00 ->  1 + 1j
# 01 -> -1 + 1j
# 11 -> -1 - 1j
# 10 ->  1 - 1j
# Dividing by sqrt(2) makes the average symbol power equal to 1.
QPSK_MAP = {
    (0, 0): (1 + 1j) / np.sqrt(2),
    (0, 1): (-1 + 1j) / np.sqrt(2),
    (1, 1): (-1 - 1j) / np.sqrt(2),
    (1, 0): (1 - 1j) / np.sqrt(2),
}


REVERSE_QPSK_MAP = {value: key for key, value in QPSK_MAP.items()}


def qpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """Map input bits to QPSK symbols."""
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)

    symbols = []
    for i in range(0, len(bits), 2):
        bit_pair = (int(bits[i]), int(bits[i + 1]))
        symbols.append(QPSK_MAP[bit_pair])

    return np.array(symbols)


def add_awgn_noise(symbols: np.ndarray, snr_db: float) -> np.ndarray:
    """Add AWGN noise according to the given SNR in dB."""
    signal_power = np.mean(np.abs(symbols) ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear

    # Complex noise has real part and imaginary part.
    # Each part takes half of the total noise power.
    noise = np.sqrt(noise_power / 2) * (
        np.random.randn(len(symbols)) + 1j * np.random.randn(len(symbols))
    )
    return symbols + noise


def qpsk_demodulate(received_symbols: np.ndarray) -> np.ndarray:
    """Demodulate QPSK symbols by checking the quadrant of each received symbol."""
    demodulated_bits = []

    for symbol in received_symbols:
        i_part = symbol.real
        q_part = symbol.imag

        if i_part >= 0 and q_part >= 0:
            demodulated_bits.extend([0, 0])
        elif i_part < 0 and q_part >= 0:
            demodulated_bits.extend([0, 1])
        elif i_part < 0 and q_part < 0:
            demodulated_bits.extend([1, 1])
        else:
            demodulated_bits.extend([1, 0])

    return np.array(demodulated_bits)


def calculate_ber(transmitted_bits: np.ndarray, received_bits: np.ndarray) -> float:
    """Calculate Bit Error Rate."""
    min_length = min(len(transmitted_bits), len(received_bits))
    transmitted_bits = transmitted_bits[:min_length]
    received_bits = received_bits[:min_length]
    return np.mean(transmitted_bits != received_bits)


def theoretical_qpsk_ber(snr_db: np.ndarray) -> np.ndarray:
    """Calculate theoretical BER for QPSK in AWGN.

    For Gray-coded QPSK, BER is the same as BPSK under the same Eb/N0.
    Here we use a simple approximation based on the Q-function.
    """
    from math import erfc

    snr_linear = 10 ** (snr_db / 10)
    return np.array([0.5 * erfc(np.sqrt(x)) for x in snr_linear])


def run_simulation() -> None:
    np.random.seed(42)

    num_bits = 100_000
    snr_db_range = np.arange(0, 13, 2)

    transmitted_bits = np.random.randint(0, 2, num_bits)
    transmitted_symbols = qpsk_modulate(transmitted_bits)

    ber_values = []
    example_received_symbols = None

    for snr_db in snr_db_range:
        received_symbols = add_awgn_noise(transmitted_symbols, snr_db)
        received_bits = qpsk_demodulate(received_symbols)
        ber = calculate_ber(transmitted_bits, received_bits)
        ber_values.append(ber)

        if snr_db == 4:
            example_received_symbols = received_symbols

        print(f"SNR = {snr_db:2d} dB, BER = {ber:.6f}")

    # Plot BER curve
    plt.figure()
    plt.semilogy(snr_db_range, ber_values, "o-", label="Simulated BER")
    plt.semilogy(snr_db_range, theoretical_qpsk_ber(snr_db_range), "--", label="Theoretical BER")
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.title("QPSK BER Performance over AWGN Channel")
    plt.grid(True, which="both")
    plt.legend()
    plt.savefig("ber_curve.png", dpi=300, bbox_inches="tight")

    # Plot constellation diagram at SNR = 4 dB
    if example_received_symbols is not None:
        plt.figure()
        plt.scatter(example_received_symbols[:1000].real, example_received_symbols[:1000].imag, s=8, alpha=0.5)
        plt.axhline(0, linewidth=1)
        plt.axvline(0, linewidth=1)
        plt.xlabel("In-phase component I")
        plt.ylabel("Quadrature component Q")
        plt.title("QPSK Received Constellation at SNR = 4 dB")
        plt.grid(True)
        plt.savefig("constellation.png", dpi=300, bbox_inches="tight")

    print("\nSimulation finished.")
    print("Generated files: ber_curve.png, constellation.png")


if __name__ == "__main__":
    run_simulation()
