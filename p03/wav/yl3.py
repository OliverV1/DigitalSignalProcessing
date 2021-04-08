import numpy as np
import scipy.io as scipy
from scipy.io import wavfile

esimene,esimene_array = scipy.wavfile.read("sample_guitar.wav")
teine,teine_array = scipy.wavfile.read("sample_violin.wav")
impulss1,impulss1_array  = scipy.wavfile.read("ir_gunshot.wav")
impulss2,impulss2_array = scipy.wavfile.read("ir_sleeping_giant_tower.wav")

listid = [esimene_array,teine_array,impulss1_array,impulss2_array]
uus = []

for i in listid:
     minimaalne_array = np.abs(np.amin(i))
     maksimaalne_array = np.amax(i)
     if maksimaalne_array > minimaalne_array:
         uus.append((i/maksimaalne_array))
     else:
         uus.append((i/minimaalne_array))


muutuja  = np.convolve(uus[0],uus[2])

if np.amax(muutuja) > np.abs(np.amin(muutuja)):
    muutuja = muutuja/np.amax(muutuja)
else:
    muutuja = muutuja / np.amax(np.abs(np.amin(muutuja)))


scipy.wavfile.write("valjud.wav", 44100, muutuja.astype(np.float32))


print("DONE")