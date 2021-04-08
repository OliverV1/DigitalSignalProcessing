import time

import numpy as np

from yl2 import myfft, ifft

from scipy.io.wavfile import read
from scipy.io.wavfile import write


def overlap_add(s1, s2):

    convolve_segment_length = 2**(int(np.log2(len(s1)))+2)

    result = np.zeros(len(s1) + len(s2) - 1)

    s2_segment_length = convolve_segment_length - len(s1) + 1

    s1 = np.pad(s1,(0,convolve_segment_length-len(s1)))

    signaal1 = np.fft.fft(s1)




      # Kui pikk on kahe signaali konvolutsioon?


    for i in range(0, len(s2), s2_segment_length):

        #s2_segment = np.zeros(convolve_segment_length)
        s2_segment = s2[i:i+s2_segment_length]
        s2_segment = np.pad(s2_segment,(0,convolve_segment_length-len(s2_segment)))

        # Signaal2 sagedusruumi
        signaal2 = np.fft.fft(s2_segment)



        convolve_segment =np.real(np.fft.ifft(np.multiply(signaal1,signaal2)))

        if len(convolve_segment)< len(result[i:]):
            result[i:i + convolve_segment_length] += convolve_segment[0:convolve_segment_length]
        else:
            result[i:i + convolve_segment_length] += convolve_segment[0:len(result) - i]


    return result


def single_impulse_convolve(amplitude, time_index, imp_response, length):
    """
    Funktsioon, mis täidab ühe alamosa konvolutsiooni sisendsignaali algoritmist
    (arvutab tulemuse sisendsignaali ühe sämpli jaoks).

    Sisendid:
    amplitude - vaatluse all oleva sisendsignaali sämpli väärtus (impulsi [0, 0, -3] puhul -3)
    time_index - vaatluse all oleva sisendsingnaali sämpli esinemise ajahetk ((impulsi [0, 0, -3] puhul 2))
    imp_response - signaal, millega konvoleeritakse (nt. [0.5, 1 , -2])
    length - tulemuseks oleva massiivi/järjendi pikkus (peab olema piisav, et tulemus mahuks ära, võib olla pikem)
    #single_impulse_convolve(0.5, 3, sig12, 7)
    Tagastab:
    result - Massiiv/järjend pikkusega 'length', milles on alates indeksist 'time_signal' väärtused 'imp_response' sisendist,
        mis on 'amplitude' väärtusega läbi korrutatud. Ülejäänud väärtused on nullid.
    """
    b = np.array(imp_response) * amplitude
    a = np.zeros(length - (np.size(b)))

    return np.insert(a, time_index, b)


def input_side_convolution(in_sig, imp_response):
    """
    Funktsioon, ise kirjutatud konvolutsiooni teostamiseks sisendsignaali algoritmi kaudu.
    Konvolutsiooni teostamiseks peab kasutama eelnevalt loodud abifunktsiooni.

    Sisendid:
    in_sig - konvolutsiooni esimene sisendsignaal
    imp_response - signaal, millega esimest signaali konvoleeritakse

    Tagastab:
    result - Massiiv/järjend sobiva pikkusega, milles on kahe sisendiks oleva signaali konvolutsiooni tulemus.
    """
    #    sig21 = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    # sig22 = [-1, 1, -1, 0, 1, -1, 1]
    pikkus = np.size(in_sig) + np.size(imp_response) - 1
    muutuja = 0
    kokku = np.zeros(pikkus)
    for i in in_sig:
        kokku = np.add(kokku, single_impulse_convolve(amplitude=i, time_index=muutuja, imp_response=imp_response,
                                                      length=pikkus))
        muutuja += 1
    return kokku
def main():
    # s1 = np.array([5, 2, 7, -10,10,10,10,10,10])
    # s2 = np.array([2, 9, 4, -4, 1, -9, 0, 3, 3,10])
    # print(np.convolve(s1, s2))
    # print(overlap_add(s1, s2))
    kitarr = read("guitar_very_short.wav")
    kitarr = np.array(kitarr[1],dtype=np.float32)
    lask = read("ir_gunshot_short.wav")
    lask = np.array(lask[1], dtype=np.float32)
    aeg1 = time.time()
    overlap_signaalidest = overlap_add(lask, kitarr)
    maksimum = np.amax(np.abs(overlap_signaalidest))
    tulemus = overlap_signaalidest/maksimum
    aeg2 = time.time()

    print("overlap add : ")
    print(aeg2-aeg1)

    minu_konvulutsioon = input_side_convolution(lask,kitarr)
    maksimum = np.amax(np.abs(minu_konvulutsioon))
    minu_konvulutsioon_tulemus = minu_konvulutsioon/maksimum
    aeg3 = time.time()

    print("Minu kovulutsioon : ")
    print(aeg3-aeg2)







    audio = tulemus.astype(np.float32)
    minu_konv_tulemus = minu_konvulutsioon_tulemus.astype(np.float32)

    write('minu_konv.wav', 8000, minu_konv_tulemus)
    write('overlap.wav', 8000, audio)  # kirjtuab faili, argumentideks- nimetus,sample rate ja teos ise



if __name__ == "__main__":
    main()
