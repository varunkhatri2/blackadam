# Black Adam
A song recognition software that uses Shazam's algorithm of audio fingerprinting

blackadam.py - the main script; execute this when the song to be recognized is playing
createdatabase.py - creates an npz database of fingerprints of all songs present in a folder
fingerprint.py - extras spectrogram peaks, creates fingerprints and stores them in hashing data structures
query.py - records audio to be recognized
search.py - searches the recorded query audio in the database

Additional libraries used: numpy, matplotlib, librosa, scipy, wave, pyaudio
