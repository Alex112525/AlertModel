import numpy as np
import matplotlib.pyplot as plt


class Circadian:
    fo = 200  # Frequency
    To = 1 / fo  # Period
    A = 0.5  # Amplitude
    theta = 1  # Phase
    count = 0

    # Frequency, Period, Sampling
    # Fs = 1000 * fo  # Sampling Frequency
    # Ts = 1 / Fs  # Sampling Period
    t = []
    x = []

    Activation = 0

    def __init__(self, samplefreq=100):
        self.Fs = samplefreq * self.fo
        self.Ts = 1 / self.Fs
        self.t = np.arange(0, self.To, self.Ts)
        self.x = self.A * np.cos(2 * np.pi * self.fo * self.t + self.theta) + 0.5

    def get_out(self):
        self.Activation = (self.A * np.cos(2 * np.pi * self.fo * self.t[self.count % len(self.t)] + self.theta) + 0.5) * 100
        self.count += 1
        return self.Activation

    def print(self):
        plt.plot(self.t, self.x)
        plt.grid("on")
        plt.show()
        print("Period:", self.t[:10])



if __name__ == "__main__":
    Cir = Circadian(100)
    Cir.print()
    cycle = []
    for n in range(10):
        cycle.append(Cir.get_out())

    print(cycle)
