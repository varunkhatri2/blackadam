from fingerprint import createfingerprint
from fingerprint import createhashes
import numpy as np
import librosa as lr
import os
import glob

server_tables = []
offset_times = []
files = []
song_names = []
extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.ogg']

for ext in extensions:
    for filename in glob.glob(os.path.join('Pop', ext)):
        files.append(filename)
        song_names.append(os.path.basename(filename))

for i in range(len(files)):

    x, fs = lr.load(files[i], sr = 8192, mono = True)
    F_print = createfingerprint(x)
    T, O = createhashes(F_print, offset = True)
    server_tables.append(T)
    offset_times.append(O)
    print(i)

np.savez('server_tables', server_tables)
np.savez('offset_times', offset_times)
np.savez('song_names', song_names)
