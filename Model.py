import Box as Box
import numpy as np
import matplotlib.pyplot as plt
import random
import Integration


def AlertModel(sample, circadian, memory, dir):
    # Vars
    samples = sample
    times = samples * 50
    frec_vec, amp_vec, time_vec = Integration.get_audio(memory)
    modes = [frec_vec, amp_vec, time_vec]
    labels = ["frec_vec", "amp_vec", "time_vec"]
    Out = []

    for i, mode in enumerate(modes):
        # Object Creation
        SCN = Box.Component("NCS", times)
        VLPO = Box.Component("VLPO", times)
        DMH = Box.Component("DMH", times)
        VTA = Box.Component("VTA", times)
        DRN = Box.Component("DRN", times)
        TMN = Box.Component("TMN", times)
        LC = Box.Component("LC", times)
        LHA = Box.Component("LHA", times)
        vPAG = Box.Component("vPAG", times)
        BF = Box.Component("BF", times, auto=True)
        PB = Box.Component("PB", times, auto=True)

        LDT = Box.Component("LDT", times)
        PPT = Box.Component("PPT", times)
        PZ = Box.Component("PZ", times)

        PFC = Box.Component("PFC", times)

        Thalamus = Box.Component("Thalamus", times, decay=True)

        Audio = Box.Component("Audio", times)

        Areas = [VLPO, DMH, VTA, DRN, TMN, LC, LHA, vPAG, BF, PB, LDT, PPT, PZ, PFC, Thalamus]

        # initialization
        SCN.set(0)
        for area in Areas:
            area.set(random.randint(10, 80))
        Audio.set(0)

        # Connections
        VLPO.connect(SCN, "map", 0.9)
        VLPO.connect(PB, "A", 0.5)
        VLPO.connect(DRN, "I", 0.33)
        VLPO.connect(TMN, "I", 0.33)
        VLPO.connect(LC, "I", 0.33)

        DMH.connect(SCN, "A", 0.9)

        TMN.connect(SCN, "A", 0.3)
        TMN.connect(DRN, "A", 0.3)
        TMN.connect(LC, "A", 0.4)
        TMN.connect(LHA, "A", 0.3)
        TMN.connect(BF, "A", 0.3)
        TMN.connect(VLPO, "I", 0.4)

        DRN.connect(LHA, "A", 0.6)
        DRN.connect(PFC, "A", 0.6)
        DRN.connect(VLPO, "I", 0.1)
        DRN.connect(PZ, "I", 0.2)
        DRN.connect(LDT, "A", 0.6)

        LC.connect(DMH, "A", 0.6)
        LC.connect(LHA, "A", 0.5)
        LC.connect(VLPO, "I", 0.3)

        LHA.connect(PB, "A")
        LHA.connect(VLPO, "I", 0.25)
        LHA.connect(PZ, "I", 0.3)

        VTA.connect(DMH, "A", 0.35)
        VTA.connect(DRN, "A", 0.35)
        VTA.connect(LDT, "A", 0.35)
        VTA.connect(DRN, "I", 0.3)
        VTA.connect(PZ, "I", 0.3)

        vPAG.connect(DRN, "A")
        vPAG.connect(DRN, "I", 0.1)
        vPAG.connect(VLPO, "I", 0.1)
        vPAG.connect(PZ, "I", 0.1)

        BF.connect(LC, "A", 0.7)
        BF.connect(PB, "A", 0.5)

        PB.connect(Thalamus, "A", 0.5)
        PB.connect(PZ, "I", 0.5)

        PFC.connect(VTA, "A", 0.15)
        PFC.connect(vPAG, "A", 0.15)
        PFC.connect(DRN, "A", 0.15)
        PFC.connect(TMN, "A", 0.15)
        PFC.connect(LC, "A", 0.2)
        PFC.connect(BF, "A", 0.15)
        PFC.connect(LHA, "A", 0.15)
        PFC.connect(Thalamus, "A", 0.3)

        LDT.connect(VLPO, "I", 0.3)
        LDT.connect(PFC, "A", 0.2)
        LDT.connect(DRN, "A", 0.2)
        LDT.connect(PPT, "A", 0.2)
        LDT.connect(LHA, "A", 0.2)

        PPT.connect(VLPO, "I", 0.2)
        PPT.connect(PZ, "I", 0.3)
        PPT.connect(LDT, "A", 0.2)
        PPT.connect(DRN, "A", 0.15)
        PPT.connect(LC, "A", 0.2)
        PPT.connect(LHA, "A", 0.15)

        PZ.connect(LHA, "A", 0.2)
        PZ.connect(PPT, "A", 0.2)
        PZ.connect(VTA, "A", 0.2)
        PZ.connect(vPAG, "A", 0.2)
        PZ.connect(DRN, "A", 0.2)

        Thalamus.connect(LDT, "A", 0.3)
        Thalamus.connect(PPT, "A", 0.3)
        Thalamus.connect(Audio, "A", 0.3)

        cir_vec = np.linspace(circadian[0], circadian[1], times)
        # Loop
        for n in range(times):
            SCN.manual_arr(cir_vec)
            Audio.manual_arr(mode)
            for area in Areas:
                area.update()
        Out.append(PFC.get_data())

        t = np.arange(0, times)
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        ax1.plot(t, SCN.get_data(), "r-", label="SCN")
        ax2.plot(t, Audio.get_data(), "b-", label="Audio")
        ax3.plot(t, Thalamus.get_data(), "g--", label="Thalamus")
        ax4.plot(t, PFC.get_data(), "c:", label="PFC")

        ax1.set_title("Circadian rhythm", fontsize='10', loc="left")
        ax2.set_title("Audio differential signal", fontsize='10', loc="left")
        ax3.set_title("Talamo Signal", fontsize='10', loc="left")
        ax4.set_title("Cortex output ", fontsize='10', loc="left")

        fig.set_figheight(10)
        fig.set_figwidth(15)

        axis = [ax1, ax2, ax3, ax4]
        for ax in axis:
            ax.grid("on")
            ax.legend()
            ax.set_yticks((0, 100, 50))
            ax.set(ylabel="Activation(%)", xlabel="Sps")
        plt.savefig(dir + "/" + labels[i] + ".svg", format='svg', dpi=1200)
        plt.close()

    return Out

"""
t = np.arange(0, times)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
 
#Plot all signals
ax1.plot(t, SCN.get_data(), "r--", label="SCN")
ax1.plot(t, VLPO.get_data(), label="VLPO(GABA)")
# ax1.plot(t, DMH.get_data(), label="DMH")
ax1.plot(t, VTA.get_data(), label="VTA(DA)")
ax2.plot(t, DRN.get_data(), "c", label="DRN(5-HT)")
ax2.plot(t, TMN.get_data(),  "g--", label="TMN(HA)")
ax2.plot(t, LC.get_data(), label="LC(NA)")
# ax2.plot(t, LHA.get_data(), label="LHA(ORX)")
ax3.plot(t, vPAG.get_data(), "b--", label="vPAG(DA)")
ax3.plot(t, BF.get_data(), label="BF(ACh)")
# ax3.plot(t, PB.get_data(), label="PB(Glu)")
ax3.plot(t, PZ.get_data(), label="PZ(GABA)")
# ax4.plot(t, PPT.get_data(), "y--", label="PPT(ACh)")
# ax4.plot(t, LDT.get_data(), "g--", label="LDT(ACh)")
ax4.plot(t, Audio.get_data(), label="Audio")
ax4.plot(t, PFC.get_data(), label="PFC")
ax4.plot(t, Thalamus.get_data(), label="Thalamus")

ax1.set_title("Ritmo circadiano e Inhibicion", fontsize='11', loc="left")
ax2.set_title("Modelado de Neurotransmisores", fontsize='11', loc="left")
ax3.set_title("Más Neurotransmisores", fontsize='11', loc="left")
ax4.set_title("Estímulo auditivo", fontsize='11', loc="left")
"""
