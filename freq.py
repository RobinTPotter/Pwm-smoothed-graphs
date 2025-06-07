import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

def gogo(pwm_freq, r, c, f):

    cutoff_freq =  1/(2*np.pi*r*c)  #15900  # Cutoff frequency of the RC filter (Hz)
    print(r,c,cutoff_freq)

    # Parameters
    fs = 100000  # Sampling frequency (100 kHz)
    duration = 0.006  # Duration of signal (seconds)

    # Time vector
    t = np.arange(0, duration, 1/fs)

    # Modulating signal (sine wave to modulate duty cycle)
    def modsig(mod_freq):
        return 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t))  # Normalized between 0 and 1


    # RC Low-pass filter (Butterworth approximation for better simulation)
    def butter_lowpass_filter(data, cutoff, fs, order=1):
        nyq = 0.5 * fs
        norm_cutoff = cutoff / nyq
        b, a = butter(order, norm_cutoff, btype='low', analog=False)
        y = lfilter(b, a, data)
        return y


    a=f[0][1]*modsig(f[0][0])
    for ff in f[1:]:
        a = np.add(a, ff[1]*modsig(ff[0]))

    mod_signal = a



    # Filter parameters

    # Plot
    plt.figure(figsize=(12, 6))




    # Updated parameters

    # Generate new PWM signal with updated carrier frequency
    pwm_signal_high_freq = (np.mod(t, 1/pwm_freq) < (mod_signal / pwm_freq)).astype(float)

    # Apply same low-pass filter to new PWM signal
    filtered_signal_high_freq = butter_lowpass_filter(pwm_signal_high_freq, cutoff_freq, fs)

    # Plot
    plt.figure(figsize=(12, 6))
    titlebit = f'{" and ".join([str(fff[0]) for fff in f])}'

    plt.subplot(2, 1, 1)
    plt.plot(t[0:1000], pwm_signal_high_freq[0:1000], label='PWM Signal (62.5 kHz Carrier)', linewidth=0.5)
    plt.title(f'PWM Signal at 62.5 kHz with {titlebit} Hz Modulated Duty Cycle')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    ax = plt.gca()
    ax.set_ylim([-0.05, 1.01])


    plt.plot(t, filtered_signal_high_freq, label='Filtered Signal (RC Output)', color='orange')
    plt.title(f'Filtered Signal Approximating a {titlebit} Hz Sine Wave')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.tight_layout()
    #plt.show()
    plt.savefig('static/sine_wave.png')



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("pwm_freq")
    parser.add_argument("r")
    parser.add_argument("c")
    parser.add_argument("freqs")

    args = parser.parse_args()

    pwm_freq = int(args.pwm_freq)  #62500  # PWM carrier frequency (62.5 kHz)
    r = float(args.r) # 500
    c= float(args.c) #47e-9

    import json
    fs = json.loads(args.freqs)
    print(fs)

    f=[]
    for ff in fs:
        f.append([int(ff), fs[ff]])

    print (f)
    gogo(pwm_freq, r, c, f)
