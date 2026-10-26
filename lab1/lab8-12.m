clear; clc; close all;

A = 2;
f = 9;
phi = pi/4;
dur = 4.035;      

[y, Fs] = audioread('voice.wav');
y = y(:, 1); 
fprintf('9) Fs %d Гц, отсчётов: %d\n', Fs, length(y));

Fs_calc = length(y) / dur;
fprintf('10) Fs = %.0f Гц (совпадает с audioread: %d Гц)\n', Fs_calc, Fs);

y1  = downsample(y, 10); 
Fs1 = Fs / 10;
fprintf('11) После прореживания: Fs = %d Гц, отсчётов: %d\n', Fs1, length(y1));

figure;
plot((0:length(y1)-1) / Fs1, y1);
title('11) Голос, прореженный в 10 раз');
xlabel('t, с'); grid on;

zvuk = audioplayer(y1, Fs1);                       
audiowrite('voice_down10.wav', y1, Fs1);

[fr0, a0] = spectrum(y,  Fs);
[fr1, a1] = spectrum(y1, Fs1);

figure;
subplot(2, 1, 1);
plot(fr0, a0);
title('12) Спектр оригинала');
xlabel('f, Гц');
grid on;
subplot(2, 1, 2);
plot(fr1, a1);
title('12) Спектр прореженного сигнала');
xlabel('f, Гц'); grid on;
   
w0_lin = fr0(find(a0 > 0.01, 1, 'last'));
w1_lin = fr1(find(a1 > 0.01, 1, 'last'));
fprintf('12) Ширина спектра (1%% от макс.): оригинал %.0f Гц, прореженный %.0f Гц\n', w0_lin, w1_lin);

function [fr, a] = spectrum(x, fs)
    N = length(x);
    X = abs(fft(x));
    a = X(1:floor(N/2)+1);
    a = a / max(a);
    fr = (0:floor(N/2)) * fs / N;
end