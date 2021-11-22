#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyvisa
from time import sleep

def main():
    # Ühendume ostsilloskoobiga kohalikult määratud hosti nime alusel
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('TCPIP::TYTI-136-DS1054::INSTR', read_termination="\n", write_termination="\n")

    # Saadame ostsilloskoobile seadete algväärtustamise käsu.
    inst.write('*RST')
    # Kuna reset võtab aega, ootame natuke.
    sleep(10)
    # Sulgeme ühenduse.
    inst.close()

if __name__ == '__main__':
    main()
