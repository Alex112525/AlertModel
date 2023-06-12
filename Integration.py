import Audio
import Memory
import matplotlib.pyplot as plt


def mapping(arr, in_min, in_max, out_min, out_max):
    map = []
    for ele in arr:
        map.append(int((ele - in_min) * (out_max - out_min) / (in_max - in_min) + out_min))
    return map


def resize(arr, sample):
    new_arr = []
    for ele in arr:
        x = [ele for x in range(sample)]
        new_arr += x
    return new_arr


def get_audio(mode="loss"):
    sample = 64
    matrix = []

    frec_vector, _, _ = Audio.Audicion.AudioAnalysis("Set1.wav")
    _, amp_vector, _ = Audio.Audicion.AudioAnalysis("Set2.wav")
    _, _, time_vector = Audio.Audicion.AudioAnalysis("Set3.wav")
    mem = Memory.Memoria(frec_vector, amp_vector, time_vector)
    if mode == "loss":
        matrix = mem.perdidaMemoria()
    if mode == "mean":
        matrix = mem.promedio()

    mem_frec = mapping(matrix[0], min(matrix[0]), max(matrix[0]), 0, 100)
    mem_amp = mapping(matrix[1], min(matrix[1]), max(matrix[1]), 0, 100)
    mem_time = mapping(matrix[2], min(matrix[2]), max(matrix[2]), 0, 100)

    mem_frec = resize(mem_frec, sample)
    mem_amp = resize(mem_amp, sample)
    mem_time = resize(mem_time, sample)

    return [mem_frec, mem_amp, mem_time]


# print(matrix)
if __name__ == "__main__":
    me_frec, me_amp, me_time = get_audio("loss")
    y = [x for x in range(50 * 64)]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(y, me_frec)
    ax2.plot(y, me_amp)
    ax3.plot(y, me_time)

    ax1.set_title("Memoria frecuencia", fontsize='11', loc="left")
    ax2.set_title("Memoria Amplitud", fontsize='11', loc="left")
    ax3.set_title("Memoria tiempo", fontsize='11', loc="left")
    plt.title("Memoria promedio")
    plt.show()
