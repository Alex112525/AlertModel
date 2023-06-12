import random


class Component:
    def __init__(self, name, reg, auto=False, n_auto=1, decay=False):
        self.Activation = 0     # Level of activation in the component
        self.No_Inputs = 0      # Number of connections
        self.N_data = 0         # Label
        self.Name = name        # Name of the component
        self.registers = reg    # Number of records
        self.auto = auto        # Auto function activate
        self.N_auto = n_auto    # Range of auto function
        self.Inputs = []        # Interconnected Areas
        self.Decay = decay      # Decay function activate
        self.Data = [0 for x in range(self.registers)]      # Data logging

    def print_data(self):
        print("Area", self.Name, "% Activation", self.Activation, "Inputs", self.No_Inputs)

    def set(self, act):
        self.Activation = act
        self.Data[self.N_data-1 % self.registers] = self.Activation

    def get_data(self):
        return self.Data

    def manual(self, start, end, signal):
        if start <= (self.N_data % self.registers) <= end:
            self.Activation = signal
        else:
            self.Activation = 0
        self.Data[self.N_data % self.registers] = self.Activation
        self.N_data += 1

    def manual_arr(self, arr):
        self.Activation = arr[self.N_data]
        self.Data[self.N_data % self.registers] = self.Activation
        self.N_data += 1

    def update(self):
        self.read_inputs()
        if self.Decay:
            self.Activation *= 0.6
            self.Activation += self.decay_func()
            self.range()
        self.Data[self.N_data % self.registers] = self.Activation
        self.N_data += 1

    def read_inputs(self):
        activation = 0
        if self.auto:
            if self.N_auto:
                activation += random.randint(-self.N_auto, self.N_auto)
        for area, mode, weight in self.Inputs:
            if mode == "A":
                activation += area.Activation * weight
            elif mode == "map":
                activation += self.map(area.Activation, 0, 100, 100, 0) * weight
            else:
                activation -= area.Activation * weight
        self.Activation = activation
        self.range()

    def connect(self, area, mode, weight=1.0):
        self.Inputs.append([area, mode, weight])
        self.No_Inputs += 1

    def decay_func(self):
        prom = sum(self.Data[self.N_data-7:self.N_data-1])/6
        return (self.mean() * 0.3) + (prom * 0.6)

    @staticmethod
    def map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def mean(self):
        total = 1
        for ele in self.Data:
            total += ele
        return total/len(self.Data)

    def range(self):
        if self.Activation < 0:
            self.Activation = 0
        elif self.Activation > 100:
            self.Activation = 100
