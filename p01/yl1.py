#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import math

# See osa loetakse sisse nii siis, kui käivitatakse otse see programmifail, kui ka siis, kui see fail on imporditud mõnda teise faili.
# Siin defineerida funktsioonid, mida saab importida ka teistesse programmidesse
def foo(x):
  return x

def bar(x):
  return x

def funktsioon1(x):
  summa = 0
  for i in range(x):
    summa += 1/math.factorial(i)
  return summa
#print(funktsioon1(6))
def funktsioon2(k = 1,a=1,r = 1):
  summa = 0
  for i in range(k):
    summa += (r**i)/a
  return summa
#print(funktsioon2(k = 10,a = 9,r = 7))

def funktsioon3(r,v):
    if (r<5 or v < 1):
      raise Exception('Vigane sisend')
    summa = 0
    for i in range(5,r+1):
      for j in range(1,v+1):
        summa += (1/np.sin(2*i))+(2*j/(3*np.pi))
    return summa
#print(funktsioon3(8,3)) #vaata -13 tehtud
def funktsioon4(a = 0,M = 0,B = 0):
  summa = 0
  b=a

  for i in range(1,26):
    for j in range(b,B+1):
      for k in range(3,M+1):
        summa += np.e**j + k*i
  return summa
#print(funktsioon4(a = 7,B=8,M=6)) #419 k sth



def funktsioon5(A=1, k = 1):
  if (A < 1):
    raise ValueError('Vigane sisend')
  summa = 1
  for i in range(1,A+1):
    summa *= (k*i)+(1/(2*k))
  return summa

#print(funktsioon5(A=7,k = 2)) #882226

def funktsioon6(C = 0, D = 0, k= 0 , l= 0):
  summa = 1
  c = k
  d = l
  if (C < k or D < l):
    raise ValueError('Vigane sisend')

  liitimine = 0
  for i in range(C):
    for k in range(D):
      if(k == D -1 ):
        liitimine +=(i+c)/(k+d)
        summa *= liitimine
        liitimine = 0
      else:
        liitimine += (i+c)/(k+d)
  return summa
#print(funktsioon6(C=5,D=1,k = 1,l = 1))

def funktsioon7(llist = []):
  summa = 0
  for i in range(len(llist)):
    summa += (3*llist[i])-7
  return summa

#print(funktsioon7(llist = [9,12,-3]))

def funktsioon8(llist= [], a = 0):
  summa = 0
  if (len(llist)<1):
    raise ValueError('Vigane sisend')


  for i in range(1,len(llist)):
    summa += llist[i-1] + llist[i]

  return a * summa

#print(funktsioon8(llist=[5,8,9], a = 4)) #120

def funktsioon9(llist = [],listikne = []):

  summa = 0
  for i in range(len(llist)):
    for j in range(len(listikne)):
      summa += llist[i]*np.cos(np.pi*listikne[j])
  return summa


#print(funktsioon9(llist= [3,8,7],listikne=[4,6,8]))



# Väga levinud tava on faili käivitamisel panna jooksutatav kood main nimelisse funktsiooni.
# Paljudes teistes keeltes on samuti main funktsioon, kus kohast algab koodi täitmine.
# https://realpython.com/python-main-function/
def main():
  x = 5
  y = foo(x)
  z = bar(y)

if __name__ == "__main__":
  # See osa loetakse sisse ainult siis, kui .py fail käivitatakse otse.
  # Kui see fail on imporditud mõnda teise programmifaili, siis teise faili käivitamisel siin olevat osa ei loeta.
  main()
