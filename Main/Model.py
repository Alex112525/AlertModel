import Box as Box
import Circadian as cr
import numpy as np
import matplotlib.pyplot as plt
import random

if __name__ == "__main__":
    # Object Creation
    Circadian = cr.Circadian(150)
    SCN = Box.Cajita("NCS")
    VLPO = Box.Cajita("VLPO")
    DMH = Box.Cajita("DMH")
    VTA = Box.Cajita("VTA")
    DRN = Box.Cajita("DRN")
    TMN = Box.Cajita("TMN")
    LC = Box.Cajita("LC")
    LHA = Box.Cajita("LHA")
    vPAG = Box.Cajita("vPAG")
    BF = Box.Cajita("BF", True, -5)
    PB = Box.Cajita("PB", True, 5)

    LDT = Box.Cajita("LDT")
    PPT = Box.Cajita("PPT")
    PZ = Box.Cajita("PZ")

    PFC = Box.Cajita("PFC")

    Thalamus = Box.Cajita("Thalamus", decay=True)

    Audio = Box.Cajita("Audio")

    Areas = [SCN, VLPO, DMH, VTA, DRN, TMN, LC, LHA, vPAG, BF, PB, LDT, PPT, PZ, PFC, Thalamus]

    # initialization
    Circadian.get_out()
    for area in Areas:
        area.set(random.randint(10, 80))
    Audio.set(0)

    # Connections
    SCN.connect(Circadian, "A", 0.9)

    VLPO.connect(SCN, "map", 0.7)
    VLPO.connect(PB, "A", 0.5)
    VLPO.connect(DRN, "I", 0.2)
    VLPO.connect(TMN, "I", 0.2)
    VLPO.connect(LC, "I", 0.2)

    DMH.connect(SCN, "A", 0.9)
    TMN.connect(SCN, "A", 0.3)
    TMN.connect(DRN, "A", 0.3)
    TMN.connect(LC, "A", 0.3)
    TMN.connect(LHA, "A", 0.3)
    TMN.connect(BF, "A", 0.3)
    TMN.connect(VLPO, "I", 0.2)

    DRN.connect(LHA, "A")
    DRN.connect(PFC, "A")
    DRN.connect(VLPO, "I", 0.2)
    DRN.connect(PZ, "I", 0.2)
    DRN.connect(LDT, "A", 0.2)

    LC.connect(DMH, "A", 0.9)
    LC.connect(LHA, "A", 0.9)
    LC.connect(VLPO, "I", 0.2)

    LHA.connect(PB, "A")
    LHA.connect(VLPO, "I", 0.1)
    LHA.connect(PZ, "I", 0.1)

    VTA.connect(DMH, "A", 0.6)
    VTA.connect(DRN, "A", 0.6)
    VTA.connect(LDT, "A", 0.2)
    VTA.connect(DRN, "I", 0.5)
    VTA.connect(PZ, "I", 0.5)

    vPAG.connect(DRN, "A")
    vPAG.connect(DRN, "I", 0.1)
    vPAG.connect(VLPO, "I", 0.1)
    vPAG.connect(PZ, "I", 0.1)

    BF.connect(LC, "A", 0.7)
    BF.connect(PB, "A")

    PB.connect(Thalamus, "A", 0.8)
    PB.connect(PZ, "I", 0.5)

    PFC.connect(VTA, "A", 0.15)
    PFC.connect(vPAG, "A", 0.15)
    PFC.connect(DRN, "A", 0.15)
    PFC.connect(TMN, "A", 0.15)
    PFC.connect(LC, "A", 0.15)
    PFC.connect(BF, "A", 0.15)
    PFC.connect(LHA, "A", 0.15)

    LDT.connect(VLPO, "I", 0.3)
    LDT.connect(PFC, "A", 0.15)
    LDT.connect(DRN, "A", 0.15)
    LDT.connect(PPT, "A", 0.2)
    LDT.connect(LHA, "A", 0.15)

    PPT.connect(VLPO, "I", 0.3)
    PPT.connect(PZ, "I", 0.2)
    PPT.connect(LDT, "A", 0.2)
    PPT.connect(DRN, "A", 0.15)
    PPT.connect(LC, "A", 0.15)
    PPT.connect(LHA, "A", 0.15)

    PZ.connect(LHA, "A", 0.2)
    PZ.connect(PPT, "A", 0.2)
    PZ.connect(VTA, "A", 0.2)
    PZ.connect(vPAG, "A", 0.2)
    PZ.connect(DRN, "A", 0.2)

    Thalamus.connect(LDT, "A", 0.2)
    Thalamus.connect(PPT, "A", 0.2)
    Thalamus.connect(Audio, "A", 0.3)

    # Vars
    results = []
    times = 200

    # Loop
    for n in range(times):
        Circadian.get_out()
        Audio.manual(110, 130, 40)
        for area in Areas:
            area.update()

    t = np.arange(0, times)
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(t, SCN.get_data(), "r--", label="SCN")
    axs[0, 0].plot(t, VLPO.get_data(), label="VLPO(GABA)")
    axs[0, 0].plot(t, DMH.get_data(), label="DMH")
    axs[0, 0].plot(t, VTA.get_data(), label="VTA(DA)")
    axs[1, 0].plot(t, DRN.get_data(), "c", label="DRN(5-HT)")
    axs[1, 0].plot(t, TMN.get_data(),  "g--", label="TMN(HA)")
    axs[1, 0].plot(t, LC.get_data(), label="LC(NA)")
    axs[1, 0].plot(t, LHA.get_data(), label="LHA(ORX)")
    axs[0, 1].plot(t, vPAG.get_data(), "b--", label="vPAG(DA)")
    axs[0, 1].plot(t, BF.get_data(), label="BF(ACh)")
    axs[0, 1].plot(t, PB.get_data(), label="PB(Glu)")
    axs[0, 1].plot(t, PZ.get_data(), label="PZ(GABA)")
    axs[1, 1].plot(t, PPT.get_data(), "y--", label="PPT(ACh)")
    axs[1, 1].plot(t, LDT.get_data(), "g--", label="LDT(ACh)")
    axs[1, 1].plot(t, Audio.get_data(), label="Audio")
    axs[1, 1].plot(t, PFC.get_data(), label="PFC")
    axs[1, 1].plot(t, Thalamus.get_data(), label="Thalamus")

    axis = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]
    for ax in axis:
        ax.grid("on")
        ax.legend()
    plt.show()