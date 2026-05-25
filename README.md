# QPSK-BER-Simulation

A beginner-friendly communication engineering simulation project using Python.

## What this project does

This project simulates a simple QPSK communication system.

Main process:

```text
random bits
-> QPSK modulation
-> AWGN noisy channel
-> QPSK demodulation
-> BER calculation
-> BER curve and constellation diagram
```

## Key communication concepts

- QPSK: Quadrature Phase Shift Keying
- AWGN: Additive White Gaussian Noise
- SNR: Signal-to-Noise Ratio
- BER: Bit Error Rate
- Constellation diagram

## How to run

Install the required Python packages:

```bash
pip install numpy matplotlib
```

Run the simulation:

```bash
python main.py
```

After running, the script will generate:

```text
ber_curve.png
constellation.png
```

## Why this project is useful

This project is suitable for communication engineering beginners. It helps you understand how digital bits are mapped to QPSK symbols, how noise affects transmission, and how BER changes as SNR increases.
