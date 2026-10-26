import numpy as np
import matplotlib.pyplot as plt

A = 2
f = 9
phi = np.pi / 4
fs = 80
N = fs
t = np.arange(N) / fs
x = A * np.sin(2 * np.pi * f * t + phi)

def dft(x):
    N = len(x)
    F = np.zeros(N, dtype=complex)
    for k in range(N):
        s = 0
        for n in range(N):
            s += x[n] * np.exp(-2j * np.pi * k * n / N)
        F[k] = s
    return F

def quantize_signal(signal, num_bits):
    levels = 2**num_bits - 1
    sig_min = np.min(signal)
    sig_max = np.max(signal)
    sig_range = sig_max - sig_min
    normalized = (signal - sig_min) / sig_range * levels
    quantized_norm = np.clip(np.round(normalized), 0, levels)
    return quantized_norm / levels * sig_range + sig_min

X_ref = np.abs(dft(x)) / N * 2     
freqs = np.arange(N) * fs / N 
half_N = N // 2
plt.figure(figsize=(10, 12))

for i, bits in enumerate([3, 4, 5, 6], start=1):
    x_quant = quantize_signal(x, bits)
    error = np.mean(np.abs(x - x_quant))
    print(f"Разрядность {bits} бит: средняя ошибка квантования = {error:.5f}")
    X_quant = np.abs(dft(x_quant)) / N * 2
    plt.subplot(4, 1, i)
    plt.plot(freqs[:half_N], X_ref[:half_N], 'b-', linewidth=1.5, label='без квантования')
    plt.plot(freqs[:half_N], X_quant[:half_N], 'r-', linewidth=1, label='с квантованием')
    plt.title(f'Разрядность {bits}')
    plt.xlabel('f, Гц')
    plt.ylabel('А')
    plt.xlim(0, fs / 2)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
plt.tight_layout()
plt.show()