#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pyvisa
import random

def generate_pulse_signal(inst):

    # Valime kanali, mida soovime seadistama hakata.
    # Käsud on siin toodud sellisel kujul nagu leiab dokumentatsioonist - proovige käsud dokumentatsioonist üles leida.
    # Suute tähtedega kujutatud osa on piisav käsu toimimiseks. Väiketähtedega osa on valikuline ja on toodud loetavuse huvides.
    inst.write(":SYSTem:CHANnel:CURrent CH2")

    # Kõigepealt paneme generaatori õigesse režiimi :source:apply kategooria käsuga.
    # Selle käsuga saab anda põhiparameetrid vastavalt dokumentatsioonis toodule.
    # Parameetrite ühikute andmisel saab kasutada detsimaaleesliiteid (SI). Ühiku ära jätmisel,
    #   kasutatakse dokumentatsioonis toodud vaikeühikut.
    # Soovi korral võib parameetrid ka vahele jätta, ka sellel juhul kasutatakse vaikeväärtust.
    # Antud näites on jäetud vahele offset parameeter, mis tähendab et vertikaalnihe on 0V.
    inst.write(":SOURce2:APPLy:PULSe 18kHz,5Vpp,,30deg")

    # Keerulisemate signaalide lisaparameetreid mida ei saa kaasa anda :source:apply käskudega,
    #   saab muuta :source:function kategooria vastava režiimi käskudega.
    # Antud näites muudame sel viisil pulssignaali täituvuse 20% peale.
    inst.write(":SOURce2:FUNCtion:PULSe:DCYCle 20%")

    # Peale seda, kui kanal on seadistatud lülitame sisse väljundi.
    # Signaaligeneraator jääb seejärel meie soovitud signaali genereerima.
    inst.write(":OUTP2 ON")


def generate_yl5_signal(inst):
    # Sarnaselt pulsi genereerimise näitega genereerige dualtone signaal
    #   komponentidega 4kHz ja 5kHz.
    inst.write(":SYSTem:CHANnel:CURrent CH2")
    inst.write(":SOUR2:APPL:DUALTone 4000,5 ")

    inst.write(":SOUR2:FUNC:DUALT:FREQ2 5000")
    #inst.write(":SOURce2:FUNCtion:DUALTone:FREQ1")
    inst.write(":OUTP2 ON")

   

def generate_yl6_1_signal(inst):
    inst.write(":SYSTem:CHANnel:CURrent CH2")
    inst.write(":SOUR2:APPL:DUALTone 50,5 ")

    inst.write(":SOUR2:FUNC:DUALT:FREQ2 500")
    #inst.write(":SOURce2:FUNCtion:DUALTone:FREQ1")
    inst.write(":OUTP2 ON")


def generate_yl6_2_signal(inst):
    string1 = ":SOUR2:APPL:DUALTone "
    vahepealne = str(random.randint(1500, 9000))
    string2=",5 "
    print(vahepealne)
    inst.write(string1+vahepealne+string2)
    string1 = ":SOUR2:FUNC:DUALT:FREQ2 "
    vahepealne = str(random.randint(1500, 9000))
    print(vahepealne)
    inst.write(string1+vahepealne)
    #inst.write(":SOURce2:FUNCtion:DUALTone:FREQ1")
    inst.write(":OUTP2 ON")


def main():
    rm = pyvisa.ResourceManager()

    # Järgneva käsuga saab loetleda kõik ühendatud seadmed. Hea viis ühenduse veaotsinguks.
    # print(rm.list_resources())

    # Ühendume läbi USB signaaligeneraatori külge ja loome klassist vastava isendi.
    usb_resources = list(filter(lambda name: 'USB' in name and 'DG8A' in name, rm.list_resources()))
    inst = rm.open_resource(usb_resources[0])

    # Ühenduse kontrolliks saab näiteks küsida seadme ID-d.
    # print(inst.query("*IDN?"))

    # TODO: Kasutage vastavalt ülesandele õiget funktsiooni kutset:
    #generate_pulse_signal(inst)  # Näide
    #generate_yl5_signal(inst)
    #generate_yl6_1_signal(inst)
    generate_yl6_2_signal(inst)

    # Sulgeme ühenduse generaatoriga, generaatori töö jätkub iseseisvalt.
    inst.close()


if __name__ == "__main__":
    main()
