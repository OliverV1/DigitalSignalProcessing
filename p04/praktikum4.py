#!/usr/bin/python3
# -*- coding: utf-8 -*-

import fourier_gui
from tasks import *
from PyQt5.QtWidgets import QApplication
import sys

import numpy as np

def f(x, k=1, A=1, phi=0, b=0):
    """
    Rakenda koosinusfunktsiooni sisendandmete peal antud parameetritega.

    Argumendid:
    x -- np massiiv sisendandmetega
    k -- sinusoidi sagedus (vaikimisi 1)
    A -- sinusoidi amplituud (vaikimisi 1)
    phi -- sinusoidi faasinihe radiaanides (nihe x-teljel) (vaikimisi 0)
    b -- sinusoidi nihe (nihe y-teljel) (vaikimisi 0)

    Tagastab:
        np.array, mis saadakse funktsiooni rakendamisel sisendandmetele

    """


    # k=2 ei mahu täielikult ekraanile, kõrgema sageudse juures
    return  (A*np.cos((2*np.pi*k*x+phi)))+b #A*np.cos(np.pi*2*(x + phi)) + b





def signal_sum(signals):
    """

    Funktsioon, mis liidab elementhaaval sisendsignaale.

    Argumendid:
    signals - np.array liidetavatest signaalidest. NB! Signaalide arv ei ole teada.

    Tagastab:
        np.array, mis saadakse sisendsignaalide elementhaaval liitmise tulemusena
    """
    uus = np.zeros((1,200))
    for i in range(np.array(signals).shape[0]):
        uus = np.add(uus,signals[i])

    return uus[0]

def compare_signals(signal1, signal2):
    """
    Funktsioon, mis arvutab kahe signaali kattuvuse skalaarkorrutisena.

    Argumendid:
    signal1, signal2 -- np.array, sisendsignaalid, mille kattuvust arvutatakse

    Tagastab:
        float arvuna signaalide skalaarkorrutise tulemus
    """
    return np.dot(signal1,signal2)

def find_frequencies(x, y):
    """
    Funktsioon, mis leiab algsignaali komponendid proovides läbi kõik võimalikud faasid ja sagedused.

    Argumendid:
    x -- ajaväärtused
    y -- algsignaal, mida analüüsitakse

    Tagastab:
        np.array kujuga (x.shape[0] + 1, 2), kus on iga sageduse jaoks leitud parim faasinihe ja selle põhjal arvutatud kattuvus
    """
    listikene=[]
    result = np.zeros((x.shape[0] + 1, 2))
    i = np.arange(0,2*np.pi,(2*np.pi)/360)
    # for j in range(0,201,1):
    #      for o in range(0,360,1):
    #          a = compare_signals(f(x, k=j, A=1, phi=i[o], b=0), y)
    #          result[j]=i[0]
    for itera in range (0,200,1):
        piiraja = 0
        for k in range(0,360,1):
            funktsioon = f(x=x, k=itera, A=1, phi=i[k], b=0)
            u1 = np.array(funktsioon)
            muutuja = compare_signals(y,u1)
            if int(muutuja) > 0.000:
                if muutuja > piiraja:
                    piiraja,index,kraadid = muutuja,itera,i[k]
        result[index]=int(np.degrees(kraadid))





    return result






"""
Mida tähendab, kui kahe signaali skalaarkorrutise väärtus on negatiivne?
kui tõmmata noolega risti vektor, siis sellest vektrosit allpool on negatiivsed väärtused
Mida tähendab, kui kahe signaali skalaarkorrutise väärtus on null?
nad kattuvad
Kuidas mõjutab faasinihe skalaarkorrutise tulemust?
Kui peakid hakkavad kattuma, on meie dorprodukt suurim
Kuidas mõjutab amplituudi või vertikaalnihke muutmine skalaarkorrutise tulemust?
mida lähemale need amplituudid satuvad, seda suurem tulemus.
"""

def main():

    STUDYBOOK_NR = "B78820" # Sisesta siia oma matriklinumber
    TASK_NR = 6# Uuenda seda muutujat vastavalt ülesandele
    RANDOM_SEED = 666         # Muuda seda numbrit, et genereerida uus juhuslike parameetritega algsignaal

    # Järgnevat koodi *ei ole* vaja muuta.
    x = np.arange(0, 1, 0.005) # Ajaväärtused, mille põhjal arvutakse algsignaal ja signaalikomponendid

    app = QApplication(sys.argv)
    task = tasklist[TASK_NR-1](studybook_nr=STUDYBOOK_NR, x=x, subtask=RANDOM_SEED)
    task.ifh.set_component_function(f)
    task.ifh.set_sum_function(signal_sum)
    task.ifh.set_compare_function(compare_signals)
    task.ifh.set_frequency_finder(find_frequencies)
    task.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()