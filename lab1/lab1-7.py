import numpy as np
import matplotlib.pyplot as plt

A = 2
f = 9

def y(t):
    return A * np.sin(2 * np.pi * f * t + np.pi / 4)

def dft(x):
    N = len(x)
    F = np.zeros(N, dtype=complex)
    for k in range(N):
        s = 0
        for n in range(N):
            s += x[n] * np.exp(-2j * np.pi * k * n / N)
        F[k] = s
    return F


t_cont = np.linspace(0, 1, 1000)
plt.figure(figsize=(8, 3))
plt.plot(t_cont, y(t_cont))
plt.title("1) Непрерывный сигнал y(t)")
plt.xlabel("t, с")
plt.grid()
plt.show()

f_max = f
print(f"2) Максимальная частота f_max = {f_max} Гц")

fs_min = 2 * f_max
print(f"3) Минимальная частота дискретизации по Котельникову: fs > {fs_min} Гц")


def process_signal(fs, label):
    print(f"\nОбработка для fs = {fs} Гц ({label})")
    N = fs
    n = np.arange(N)
    t_disc = n / fs
    x = y(t_disc)
    F = dft(x)                     
    amp = np.abs(F) / N
    k = np.arange(N)
    freq = k * fs / N
    freq[freq > fs / 2] = freq[freq > fs / 2] - fs      
    threshold = 0.1 * np.max(amp)
    valid_pos_freqs = freq[(amp > threshold) & (freq >= 0)]
    if len(valid_pos_freqs) > 0:
        spectrum_width = valid_pos_freqs.max()
    else:
        spectrum_width = 0.0
        
    memory_bytes = x.nbytes
    
    print(f"4) Число отсчетов N = {N}. Объем памяти = {memory_bytes} байт (float64)")
    print(f"5) Ширина спектра = {spectrum_width:.2f} Гц")
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t_cont, y(t_cont), label="Оригинал", alpha=0.7)
    plt.stem(t_disc, x, linefmt="r-", markerfmt="ro", basefmt=" ", label="Отсчёты")
    plt.title(f"4) Оцифровка, fs = {fs} Гц")
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 2)
    order = np.argsort(freq)       
    plt.stem(freq[order], amp[order], linefmt="b-", markerfmt="bo", basefmt=" ")
    plt.title("5) Амплитудный спектр (двусторонний)")
    plt.xlabel("f, Гц")
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(t_cont, y(t_cont), label="Оригинал", alpha=0.7)
    plt.plot(t_disc, x, "g-o", label="Восстановленный по отсчётам")
    plt.title("6) Восстановление сигнала")
    plt.xlabel("t, с")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


fs1 = 2 * f + 1
process_signal(fs1, "базовая")

fs2 = fs1 * 4
process_signal(fs2, "увеличенная в 4 раза")