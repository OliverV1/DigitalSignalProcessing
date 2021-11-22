#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyvisa
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
from time import sleep
from pyqtgraph.Qt import QtGui, QtCore
from scipy.io.wavfile import write

def wait_until_ready_to_trigger(inst):
    while(True):
        # Kui ostsilloskoop ootab sünkronisatsioonisignaali, on 'Trigger:Status' parameetri väärtus 'wait'
        val = inst.query(':TRIGger:STATus?')
        print(val)
        if val == 'WAIT':
            break
        sleep(0.1)

def wait_until_measurement_done(inst):
    while(True):
        # Kui teeme 'single' tüüpi mõõtmise, lõpetab ostsilloskoop soovitud andmemahu täitumisel
        # ise mõõtmise ja 'Trigger:Status' parameetri väärtuseks saab 'Stop'
        val = inst.query(':TRIGger:STATus?')
        print(val)
        if val == 'STOP':
            break
        sleep(0.1)

def main():
    # Ühendume ostsilloskoobiga kohalikult määratud hosti nime alusel
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('TCPIP::TYTI-136-DS1054::INSTR', read_termination="\n", write_termination="\n")
    inst.write('*RST')
    sleep(9)
    # Veendume, et ainult kolmas kanal oleks aktiivne.
    inst.write(':CHANnel1:DISPlay 0')
    inst.write(':CHANnel2:DISPlay 0')
    inst.write(':CHANnel3:DISPlay 1')
    inst.write(':CHANnel4:DISPlay 0')

    # Ostsilloskoobi mälu sügavust saab muuta ainult mittepeatatud olekus.
    inst.write(':RUN')

    # Määrame ära, et soovime korraga hõivata 600,000 andmepunkti.
    inst.write(':ACQuire:MDEPth 600000')

    # Seiskame ostsilloskoobi.
    inst.write(':STOP')

    # Samuti kustutame eelnevate mõõtmiste andmed ostsilloskoobi mälust:
    inst.write(':CLEAR')

    # Seame ajalise jaotise suuruseks 500 ms, sedasi mõõdame kokku 12x0.5s = 6s
    # selle aja jooksul salvestatakse meie küsitud 600,000 andmepunkti.
    inst.write(':TIMebase:MAIN:SCALe 0.5')

    # Määrame ajalise nihke nii, et mõõdame ainult sünkroniseerimispunktile (trigger) järgnevat osa.
    inst.write(':TIMebase:MAIN:OFFSET 0.0')
    inst.write(':TIMebase:OFFSET 3')  # Selleks peame nihutama 6 jaotist ehk 3 s

    # Mikrofoni võimendi väljastatav amplituud on 2Vpp, selle põhjal määrame sobiva vertikaalse jaotuse
    # nii, et kasutaksime ära maksimaalse osa mõõteulatusest.
    inst.write(':CHANnel3:SCALE 0.1V')

    # Määrame ära ka signaali vertikaalse nihke, nii, et signaal oleks mõõtepiirkonna keskel.
    # Kasutatava mikrofoni puhul on vertikaalne nihe 1.25V.
    inst.write(':CHANnel3:OFFSET -0.1V')

    sleep(0.2) # Veendume, et ostsilloskoobil on piisavalt aega kõigi saadud käskude töötlemiseks.
    # Teeme eelnevalt määratud parameetritega ühe mõõtmise.
    inst.write(':SINGLE')

    # Kui ostsilloskoop on valmis, saadame ka käsitsi sünkroniseerimissignaali, vältimaks olukorda,
    # kus me ei alusta mõõtmist kuna meie signaal ei ületa kunagi sünkroniseerimislävendit.
    wait_until_ready_to_trigger(inst)
    inst.write(':TFORce')

    # Ootame, et mõõtmine saaks tehtud ja ostsilloskoop oleks uuesti peatatud režiimis.
    wait_until_measurement_done(inst)

    # Nüüd saame alustada andmete lugemist oma Python programmi.
    # Selleks esmalt määrame, mis kujul soovime andmeid saada.
    inst.write(':WAV:SOUR CHAN3')  # Mis kanali infot loeme.
    inst.write(':WAV:MODE RAW')  # Loeme mälust toorandmeid.
    inst.write(':WAV:FORM BYTE')  # Andmed küsime byte kujul (8-bitine resolutsioon).

    # Korraga saame lugeda maksimaalselt 250,000 andmepunkti, seega teostame 600,000 punkti lugemise kolmes osas.
    inst.write(':WAV:START 1')  # Andmete lugemise algusindeks seadme mälus.
    inst.write(':WAV:STOP 200000')  # Andmete lugemise lõppindeks seadme mälus.
    # Järgnev käsk teostab andmete lugemise.
    waveform_datapoints1 = inst.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)

    # kordame sama järgmiste osade jaoks.
    inst.write(':WAV:START 200001')
    inst.write(':WAV:STOP 400000')
    waveform_datapoints2 = inst.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)
    inst.write(':WAV:START 400001')
    inst.write(':WAV:STOP 600000')
    waveform_datapoints3 = inst.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)

    # Ühendame andmed üheks tervikuks.
    waveform_datapoints = np.concatenate((waveform_datapoints1, waveform_datapoints2, waveform_datapoints3))

    # Küsime ka info vertikaalse refernetsi kohta.
    # See näitab, millisele väärtusele saadud 8-bitistes arvudes vastab null-pinge.
    y_ref = inst.query('WAV:YREF?')

    # Kontrollimiseks kuvame saadud andmed graafikul.
    p = pg.plot(waveform_datapoints)
    p.setWindowTitle('Mõõtmise tulemus')
    p.setLabel('bottom', 'Indeks', units='Sa')
    curve = p.plot(pen='y')
    p.showGrid(x=True, y=True)

    ######## Ülesanne 2 - vaadelge saadud andmehulka ja kirjutage see peale normaliseerimist, koos õigete parameetritega, .wav faili. ########
    waveform_datapoints = waveform_datapoints-int(y_ref)
    #note = waveform_datapoints / np.max(np.abs(waveform_datapoints))#-1 kuni 1
    note = waveform_datapoints/np.max(np.abs(waveform_datapoints))
    note = note.astype(np.float32)
    write('yl6.wav', 100000, note)  # sample rate 1000000000

    QtGui.QApplication.instance().exec_()
    inst.close()

if __name__ == '__main__':
    main()
