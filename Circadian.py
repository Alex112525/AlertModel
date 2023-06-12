import numpy as np
import matplotlib.pyplot as plt


class Circadian:
    fo = 20  # Frequency
    To = 1 / fo  # Period
    A = 0.42  # Amplitude
    theta = 1  # Phase
    count = 0

    # Frequency, Period, Sampling
    t = []
    x = []

    Activation = 0

    def __init__(self, samplefreq=100):
        self.Fs = samplefreq * self.fo  # Fs = 1000 * fo  # Sampling Frequency
        self.Ts = 1 / self.Fs           # Ts = 1 / Fs  # Sampling Period
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
    Cir = Circadian(10)
    Cir.print()
    cycle = []
    for n in range(10):
        cycle.append(Cir.get_out())

    print(cycle)
