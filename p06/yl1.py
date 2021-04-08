#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

def algebraic_to_exponent(c):
    """
    Funktsioon, mis võtab sisendiks kompleksarvu algebralisel
    kujul ning tagastab sama arvu eksponentkujul.

    Sisend: complex tüüpi arv

    Väljund: tuple kujul (kompleksarvu magnituud, kompleksarvu faas)
    """

    return np.sqrt(np.real(c)**2+np.imag(c)**2),np.arctan2(np.imag(c),np.real(c))


def exponent_mult(r1, theta1, r2, theta2):
    """
    Funktsioon, mis võtab sisendiks 2 kompleksarvu eksponentkujul
    ning tagastab nende korrutise eksponentkujul

    Sisend: kaks kompleksarvu kujul tuple (magnituud, faas)

    Väljund: kompleksarv kujul tuple (magnituud, faas)
    """
    return (r1*r2,(theta1+theta2)%360)


def exponent_to_algebraic(c):
    """
    Funktsioon, mis võtab sisendiks kompleksarvu eksponentkujul
    ning tagastab sama arvu algebralisel kujul.

    Sisend: tuple kujul (kompleksarvu magnituud, kompleksarvu faas)

    Väljund: complex tüüpi arv
    """
    return complex(c[0]*np.cos(c[1]),c[0]*np.sin(c[1]))


def complex_roots(n):
    """
    Funktsioon, mis võtab sisendiks naturaalarvu n ning
    tagastab kõik arvu 1 n-juured.

    Näidissisend: 4

    Näidisväljund: [1, j, -1, -j]
    """
    tulemus = []
    for i in range(n):
        tulemus.append(np.exp(2*np.pi*1j*i/n))
    return tulemus

def main():
    # print(complex(1,2)+complex(3,-4)-complex(-2,-0.4))
    # print(complex(-1,0)+complex(0,1)+complex(1,2)+complex(5,5)+complex(-5,2))
    # print((complex(-5,-4)*complex(9,7))/complex(-10,1))
    # print((complex(-6,-8)/complex(7,-4))*complex(-10,-8))
    #print(algebraic_to_exponent(complex(3,4)))
    print(exponent_mult(1.5,90,5,-60))
    print(exponent_to_algebraic(algebraic_to_exponent(complex(3,-180))))
    print(complex_roots(5))
if __name__ == "__main__":
    main()
