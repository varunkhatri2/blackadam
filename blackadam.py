import librosa as lr
import numpy as np
import fingerprint as fp
from search import fetchID
import matplotlib.pyplot as plt
from query import recordaudio

print('Search Songs with BlackAdam!')
x = recordaudio()
# x, fs = lr.load('TestQuery/fada_orig.wav', sr = 8192, mono = True)
print('* searching *')
clip = fp.createfingerprint(x)
clip_table = fp.createhashes(clip)
name = fetchID(clip_table)
print('The song name is:')
print(name)
plt.show()
