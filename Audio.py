# Developed by Gustavo Palacios Ramirez
# gustavo.palacios@cinvestav.com

import numpy as np
# from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.io import wavfile
from os.path import join as pjoin
# import scipy.io
import os


class Audicion:
    @staticmethod
    def find_max(a, lower_bound):
        # Finds max above threshold
        # Find indexes which are above threshold
        valid_idx = np.where(a >= lower_bound)[0]

        if valid_idx.size > 0:
            # Find maximum from these indexes
            max_idx = valid_idx[a[valid_idx].argmax()]
            return max_idx, a[max_idx]  # return max value
        else:
            return 0, 0

    @staticmethod
    def AudioAnalysis(wavFileName):
        # Obtenemos el path del programa para grabar el archivo ahi
        data_dir = pjoin(os.path.dirname(os.path.realpath(__file__)), 'AudioSource')
        # wav_fname = pjoin(data_dir, 'Set1(2).wav')
        wav_fname = pjoin(data_dir, wavFileName)

        # Lectura de archivo de audio,
        samplerate, normalized_tone = wavfile.read(wav_fname)
        # Duración del archivo. Número de muestras / muestras por segundo
        length = normalized_tone.shape[0] / samplerate
        # print("Length: ", length)
        numberOfSamples = 0.5 * samplerate
        numberOfSamples = int(numberOfSamples)
        totalSamples = normalized_tone.shape[0]
        # print(numberOfSamples)
        heardFrequencies = []
        dbValues = []
        soundTimesStart = []
        soundTimesEnd = []
        startIndex = 0
        endIndex = 0
        silenceFlag = False
        threshold = -100.0
        soundTimes = []

        normalized_tone2 = np.abs(normalized_tone).astype(np.uint16)
        '''===============================Análisis de Duración========================'''
        for x in range(totalSamples):
            if normalized_tone2[x] == 0:
                maxDB = 20 * np.log(np.finfo(float).eps / 32767)
            else:
                maxDB = 20 * np.log(normalized_tone2[x] / 32767)
            if silenceFlag:
                if maxDB > threshold:
                    if startIndex == endIndex:
                        endIndex = x
                    else:
                        y = x + 1
                        if y < totalSamples:
                            if normalized_tone2[y] == 0:
                                maxDBY = 20 * np.log(np.finfo(float).eps / 32767)
                            else:
                                maxDBY = 20 * np.log(normalized_tone2[y] / 32767)
                            if maxDBY > threshold:
                                silenceFlag = False
                                soundTimesStart.append(startIndex)
                                soundTimesEnd.append(x - 1)
                                startIndex = x
                                endIndex = x
                            else:
                                endIndex = startIndex
            else:
                # Estoy en modo sonido, verificar umbral
                if maxDB <= threshold:
                    # Bajo el umbral podría ser un falso positivo, verificar condiciones.
                    # Si el punto de inicio y fin son el mismo, es la primera vez que se encuentra un silencio, reajustar final
                    if startIndex == endIndex:
                        endIndex = x
                    # De lo contrario, ya había sido encontrado un silencio, verificar siguiente dato antes de registrar y pasar a modo silencio
                    else:
                        y = x + 1
                        if y < totalSamples:
                            if normalized_tone2[y] == 0:
                                maxDBY = 20 * np.log(np.finfo(float).eps / 32767)
                            else:
                                maxDBY = 20 * np.log(normalized_tone2[y] / 32767)
                            if maxDBY <= threshold:
                                silenceFlag = True
                                soundTimesStart.append(startIndex)
                                soundTimesEnd.append(x - 1)
                                startIndex = x
                                endIndex = x
                            else:
                                endIndex = startIndex

        if startIndex == endIndex:
            soundTimesStart.append(startIndex)
            soundTimesEnd.append(totalSamples - 1)
        for x in range(len(soundTimesStart)):
            length = (soundTimesEnd[x] - soundTimesStart[x]) / samplerate
            length = np.round(length, 2)
            soundTimes.append(length)

        soundTimes = np.round(soundTimes, 2)
        result = np.where(soundTimes <= 0.01)
        result = result[0]

        soundTimes = np.delete(soundTimes, result)
        soundTimesStart = np.delete(soundTimesStart, result)
        soundTimesEnd = np.delete(soundTimesEnd, result)

        for x in range(len(soundTimes)):
            start = soundTimesStart[x]
            end = soundTimesEnd[x]
            numberOfSamples = end - start
            # print(start, end)
            normalized_tone2 = normalized_tone[start:end]

            '''===============================Análisis de Frecuencia========================'''
            yf = rfft(normalized_tone2, norm="forward")
            xf = rfftfreq(numberOfSamples, 1 / samplerate)

            # Se busca la frecuencia con el mayor aporte y su posición en el arreglo
            absMagnitude = np.abs(yf) / numberOfSamples
            maxValue = Audicion.find_max(absMagnitude, 0.1)
            frequency = xf[maxValue[0]]
            heardFrequencies.append(frequency)

            '''===============================Análisis de Amplitud========================'''
            # 32767
            absTone = np.abs(normalized_tone2)
            # print(np.max(absTone))
            # maxDB = 20 * np.log(np.max(absTone) / 32767)
            maxDB = 20 * np.log(np.mean(absTone) / 32767)
            # print("Max DB: ", maxDB)
            dbValues.append(maxDB)

        heardFrequencies = np.round(heardFrequencies, 0)
        dbValues = np.round(dbValues, 2)

        # print(len(heardFrequencies))
        # print(len(dbValues))
        # print(len(soundTimes))

        return heardFrequencies, dbValues, soundTimes
