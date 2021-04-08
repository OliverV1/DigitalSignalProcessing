import numpy as np
import simpleaudio as sa
from scipy.io.wavfile import write
import random




#https://realpython.com/playing-and-recording-sound-python/

frequency = 440 #sagedus
fs = 44100 #sample rate
seconds = 2 # pikkus 


t = np.linspace(0, seconds, seconds * fs, False) # loome listi 


note = np.sin(frequency * t * 2 * np.pi) #laine on siinus ja arvestame eeltoodud muutujatega


audio = note * (2**15 - 1) / np.max(np.abs(note)) #kõrgeim väärtus oleks 16 biti skaalas
audio = audio.astype(np.int16)

write('yl1.wav', fs, audio) # kirjtuab faili, argumentideks- nimetus,sample rate ja teos ise


#2yl
kuma = np.array([1,1,2.1,0.2,0.25,0.30,0.55,0.3,0.25,0,0.05,0.06,0,0,0,0,0]) #OBOE
note = np.convolve(note,kuma) #lisame oboe tämbri meie loodule
audio = note * (2**15 - 1) / np.max(np.abs(note)) #kõrgeim väärtus oleks 16 biti skaalas
audio = audio.astype(np.int16)

write('yl2.wav', fs, audio)# kirjtuab faili, argumentideks- nimetus,sample rate ja teos ise




#3yl
seconds = 0.5 # muudame pikkust, et ei peaks kulutame liiga kaua aega kuulamisele


#siin defineeritud noodid
def B():
    frequency = 493.88
    t = np.linspace(0, seconds, seconds * fs, False) 
    note = np.sin(frequency * t * 2 * np.pi)
    return note

def C():
    frequency = 261.63
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def D():
    frequency = 293.66
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def A():
    frequency = 440.00
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def G():
    frequency = 392.00
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def E():
    frequency = 329.63
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def P():
    frequency = 0
    t = np.linspace(0, seconds, seconds * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note
def ERI(): # kui mitu sama nooti järjest, vaja neid eristada
    frequency = 0
    t = np.linspace(0, 0.05, 0.05 * fs, False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note

kokku = np.array([0]) #loome array kuhu salvestakse nootidid
kuma = np.array([1,1,2.1,0.2,0.25,0.30,0.55,0.3,0.25]) #OBOE

kokku = np.append(kokku,np.array(G())) #lisame noodid listi
kokku = np.append(kokku,np.array(ERI())) # kaks sama nooti järjest, vaja väike paus nende vahel. Nii võimalik paremini eristada
kokku = np.append(kokku,np.array(G()))
kokku = np.append(kokku,np.array(D()))
kokku = np.append(kokku,np.array(ERI()))
kokku = np.append(kokku,np.array(D()))

kokku = np.append(kokku,np.array(E()))
kokku = np.append(kokku,np.array(ERI()))
kokku = np.append(kokku,np.array(E()))
kokku = np.append(kokku,np.array(D()))
kokku = np.append(kokku,np.array(P()))

kokku = np.append(kokku,np.array(C()))
kokku = np.append(kokku,np.array(ERI()))
kokku = np.append(kokku,np.array(C()))
kokku = np.append(kokku,np.array(B()))
kokku = np.append(kokku,np.array(ERI()))
kokku = np.append(kokku,np.array(B()))

kokku = np.append(kokku,np.array(A()))
kokku = np.append(kokku,np.array(ERI()))
kokku = np.append(kokku,np.array(A()))
kokku = np.append(kokku,np.array(G()))
kokku = np.append(kokku,np.array(P()))


note = np.convolve(kuma,kokku) # lisame oboe tämbri
audio = note * (2**15 - 1) / np.max(np.abs(note)) # jääks 16 bit vahemiku
audio = audio.astype(np.int16)

write('yl3.wav', fs, audio)



















