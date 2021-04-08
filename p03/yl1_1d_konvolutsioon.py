#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


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
    b = np.array(imp_response)*amplitude
    a = np.zeros(length-(np.size(b)))
    
    return np.insert(a,time_index,b)


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
    #sig22 = [-1, 1, -1, 0, 1, -1, 1]
    pikkus = np.size(in_sig)+np.size(imp_response)-1
    muutuja = 0
    kokku = np.zeros(pikkus)
    for i in in_sig:
       kokku = np.add(kokku,single_impulse_convolve(amplitude=i, time_index=muutuja, imp_response=imp_response, length=pikkus))
       muutuja +=1
    return kokku


def main():
    # Testide plokk ülesande esimese poole (funktsiooni single_impulse_convolve) kontrollimiseks:
    # Omalt poolt võib kontrollimiseks lisada vahe- ja lõpptulemuste väljastamist ekraanile, kuvamist graafikul jms.
    #test
    # Testsignaalid implementatsiooni katsetamiseks:
    # Soovi korral võib sisendid konverteerida kohe numpy massiivideks (np.array(minu_list)).
    sig11 = [0.5, 1, 2, 1, -1, -1]
    sig12 = [-1, 2, -1]
    # Oma implementatsiooni võrdlemine numpy konvolutsiooniga. Erinevuste korral lõpetatakse programmi töö 'AssertionError'ga:
    # kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.

    #print(np.array(single_impulse_convolve(0.5, 3, sig12, 7)))
    #print(np.convolve(sig12, [0, 0, 0, 0.5, 0]))
    
    np.testing.assert_array_equal(np.array(single_impulse_convolve(3, 2, sig11, 8)), np.convolve(sig11, [0, 0, 3]))
    np.testing.assert_array_equal(np.array(single_impulse_convolve(-2, 0, sig12, 3)), np.convolve(sig12, [-2]))
    np.testing.assert_array_equal(np.array(single_impulse_convolve(0.5, 3, sig12, 7)), np.convolve(sig12, [0, 0, 0, 0.5, 0]))

    #print(single_impulse_convolve(amplitude=0.5, time_index=3, imp_response=[1, 0.5, 0, -1, -0.3, 0.5], length=9))
    #[0, 0, 0, 0.5, 0.25, 0, -0.5, -0.15, 0.25]
    # Kui kõik kontrollid olid edukad jõuame järgmise käsuni:
    print("Kõik alamfunktsiooni testid edukalt läbitud!")
    
    # Testide plokk ülesande teise osa (funktsiooni input_side_convolution) kontrollimiseks:
    
    # Testsignaalid implementatsiooni katsetamiseks
    sig21 = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    sig22 = [-1, 1, -1, 0, 1, -1, 1]
    sig23 = [4, 4, 4, 4, 3, 3, 3]
    sig24 = [2, 1, 3]

    # Oma implementatsiooni võrdlemine numpy konvolutsiooniga. Erinevuste korral lõpetatakse programmi töö 'AssertionError'ga:
    # kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.

    np.testing.assert_array_equal(np.array(input_side_convolution(sig21, sig22)), np.convolve(sig21, sig22))
    np.testing.assert_array_equal(np.array(input_side_convolution(sig22, sig23)), np.convolve(sig22, sig23))
    np.testing.assert_array_equal(np.array(input_side_convolution(sig23, sig24)), np.convolve(sig23, sig24))
    np.testing.assert_array_equal(np.array(input_side_convolution(sig24, sig21)), np.convolve(sig24, sig21))

    # Kui kõik kontrollid olid edukad jõuame programmi lõpuni:
    print("Kõik testid edukalt läbitud!")
    
    


if __name__ == "__main__":
    main()
