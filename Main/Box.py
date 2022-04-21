import random

import numpy as np


class Cajita:
    Name = ""
    Activation = 0
    No_Inputs = 0
    auto = False
    N_auto = 1
    N_data = 0
    registers = 200
    Decay = False

    def __init__(self, name, auto=False, n_auto=1, decay=False):
        self.Name = name
        self.auto = auto
        self.N_auto = n_auto
        self.Inputs = []
        self.Decay = decay
        self.Data = [0 for x in range(self.registers)]

    def print_data(self):
        print("Area" , self.Name, "% Activation", self.Activation, "Inputs", self.No_Inputs)

    def set(self, act):
        self.Activation = act
        self.Data[self.N_data-1 % self.registers] = self.Activation

    def get_act(self):
        return self.Activation

    def get_data(self):
        return self.Data

    def manual(self, start, end, signal):
        if start <= (self.N_data % self.registers) <= end:
            self.Activation = signal
        else:
            self.Activation = 0
        self.Data[self.N_data % self.registers] = self.Activation
        self.N_data += 1

    def update(self):
        self.read_inputs()
        if self.Decay:
            self.Activation += self.decay_func()
        self.Data[self.N_data % self.registers] = self.Activation
        self.N_data += 1

    def read_inputs(self):
        activation = 0
        if self.auto:
            if self.N_auto < 0:
                activation += random.randint(self.N_auto, 0)
            else:
                activation += random.randint(0, self.N_auto)
        for area, mode, weight in self.Inputs:
            if mode == "A":
                activation += area.Activation * weight
            elif mode == "map":
                activation += self.map(area.Activation, 0, 100, 100, 40) * weight
            else:
                activation -= area.Activation * weight
        self.Activation = activation
        self.range()

    def connect(self, area, mode, weight=1.0):
        self.Inputs.append([area, mode, weight])
        self.No_Inputs += 1

    def decay_func(self):
        # return sum(self.Data[self.N_data-4:self.N_data-1])/4 * 0.90
        return sum(self.Data[self.N_data-4:self.N_data-1])/4 * np.exp(-(self.map(self.Data[self.N_data-1], 0, 100, 1, 1/1.2)))

    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def range(self):
        if self.Activation < 0:
            self.Activation = 0
        elif self.Activation > 100:
            self.Activation = 100


# if __name__ == '__main__':
#     NCS = Cajita("NCS")
#     NCS.print_data()
#
#     VLPO = Cajita("VLPO")
#     VLPO.update(50)
#     VLPO.print_data()
#
#     NCS.connect(VLPO, "A", .8)
#     NCS.read_inputs()
#     NCS.print_data()
