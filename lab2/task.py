import math
import numpy as np
import matplotlib.pyplot as plt

n_anten = 2
tx_power_ue = 24
feeder_loss = 0.5 + 0.4 + 2
ant_gain_bs = 21
mimo_gain = 10 * math.log10(n_anten)
im = 1 
penetration_m = 15
BW_UL = 10 * 10 ** 6
BW_DL = 20 * 10 ** 6
noise_figure_bs = 2.4
reqired_sinr_ul = 4

tx_power_bs = 46
noise_figure_ue = 6
reqired_sinr_dl = 2

freq_range = 1.8
d = np.linspace(0.01, 10, 10000)
A = 46.3
B = 33.9
h_bs = 30
h_ms = 1.5
Lclutter = 0 # городская застройка

delta_h = 20
w_street = 20
b_distance = 30
phi = 45

area_macro = 100.0   
area_femto = 4.0     

thermal_noise_ul = -174 + 10 * math.log10(BW_UL)
rx_sens_bs = noise_figure_bs + thermal_noise_ul + reqired_sinr_ul
mapl_ul = tx_power_ue - feeder_loss + ant_gain_bs + mimo_gain - rx_sens_bs - im - penetration_m

thermal_noise_dl = -174 + 10 * math.log10(BW_DL)
rx_sens_ue = noise_figure_ue + thermal_noise_dl + reqired_sinr_dl
mapl_dl = tx_power_bs - feeder_loss + ant_gain_bs + mimo_gain - rx_sens_ue - im - penetration_m

PL_UMiNLOS = 26 * np.log10(freq_range) + 22.7 + 36.7 * np.log10(d * 1000)

s_high = 44.9 - 6.55 * np.log10(freq_range * 1000)
s_low = (47.88 + 13.9 * np.log10(freq_range * 1000) - 13.9 * np.log10(h_bs)) * (1/np.log10(50))
a_hms = 3.2 * ((np.log10(11.75 * h_ms)) ** 2) - 4.97 # городская застройка
s = np.where(d >= 1, s_high, s_low)
PL_COST231 = A + B * np.log10(freq_range * 1000) - 13.82 * np.log10(h_bs) - a_hms + s * np.log10(d) + Lclutter

L_LOS = 42.6 + 20 * np.log10(freq_range * 1000) + 26 * np.log10(d)
L0 = 32.44 + 20 * np.log10(freq_range * 1000) + 20 * np.log10(d)
L2 = -16.9 - 10 * np.log10(w_street)  + 10 * np.log10(freq_range * 1000) + 20 * np.log10(delta_h - h_ms) + 2.5 + 0.075 * phi
L11 = -18 * np.log10(1 + h_bs - delta_h)
Ka = 54 # h_bs > delta_h
Kd = 18 # h_bs > delta_h
Kf = -4 + 0.7 * ((freq_range * 1000) / 925 - 1)
L1 = L11 + Ka + Kd * np.log10(d) + Kf * np.log10(freq_range * 1000) - 9 * np.log10(b_distance)
L_NLOS = np.where(L1 + L2 > 0, L0 + L1 + L2, L0)

def find_radius(PL, mapl):
    return float(np.interp(mapl, PL, d))
d_ul_hata = find_radius(PL_COST231, mapl_ul)
d_dl_hata = find_radius(PL_COST231, mapl_dl)
R_macro = min(d_ul_hata, d_dl_hata)          
S_macro = 1.95 * R_macro ** 2                
N_macro = math.ceil(area_macro / S_macro)
d_ul_umi = find_radius(PL_UMiNLOS, mapl_ul)
d_dl_umi = find_radius(PL_UMiNLOS, mapl_dl)
R_femto = min(d_ul_umi, d_dl_umi)
S_femto = 1.95 * R_femto ** 2
N_femto = math.ceil(area_femto / S_femto)

print('Задание 1')
print(f'MAPL_UL = {mapl_ul:.2f} дБ')
print(f'ThermalNoiseUL = {thermal_noise_ul:.2f}')
print(f'RxSensBS = {rx_sens_bs:.2f} дБм \n') 
print('Задание 2')
print(f'MAPL_DL = {mapl_dl:.2f} дБ')
print(f'ThermalNoiseDL = {thermal_noise_dl:.2f}')
print(f'RxSensUE = {rx_sens_ue:.2f} дБм\n')
print('Задание 4')
print('Макросеть (COST231-Hata):')
print(f'd_UL = {d_ul_hata:.3f} км')
print(f'd_DL = {d_dl_hata:.3f} км')
print(f'радиус R = {R_macro:.3f} км')
print(f'площадь сайта S = {S_macro:.3f} кв.км')
print(f'требуется БС N = {N_macro}\n')
print('Микро-фемтосеть (UMiNLOS):')
print(f'd_UL = {d_ul_umi:.3f} км')
print(f'd_DL = {d_dl_umi:.3f} км')
print(f'радиус R = {R_femto:.3f} км')
print(f'площадь сайта S = {S_femto:.3f} кв.км')
print(f'требуется БС N = {N_femto}')


plt.title("Задание 3")
plt.plot(d, PL_UMiNLOS, label='UMiNLOS (1.8 ГГц)', color='blue')
plt.plot(d, PL_COST231, label='COST231-Hata (1.8 ГГц)', color='orange')
plt.plot(d, L_NLOS, label='Walfish-Ikegami (L_NLOS) (1.8 ГГц)', color='purple' )
plt.plot(d, L_LOS, label='Walfish-Ikegami (L_LOS) (1.8 ГГц)', color='black' )
plt.axhline(y=mapl_ul, linestyle='--', label='MAPL_UL', color='green')
plt.axhline(y=mapl_dl, linestyle='--', label='MAPL_DL', color='red')
plt.plot([d_ul_umi, d_dl_umi], [mapl_ul, mapl_dl], 'o', color='darkblue', markersize=8, zorder=5, label='Пересечения UMiNLOS')
plt.plot([d_ul_hata, d_dl_hata], [mapl_ul, mapl_dl], 'o', color='darkorange', markersize=8, zorder=5, label='Пересечения Hata')
plt.xlabel('Расстояние между приемником и передатчиком, км')
plt.ylabel('Потери сигнала, дБ')
plt.grid(True)
plt.legend()
plt.show()


