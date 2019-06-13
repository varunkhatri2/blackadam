# Black Adam
A song recognition software that uses Shazam's algorithm of audio fingerprinting

blackadam.py - the main script; execute this when the song to be recognized is playing <br />
createdatabase.py - creates an npz database of fingerprints of all songs present in a folder <br />
fingerprint.py - extras spectrogram peaks, creates fingerprints and stores them in hashing data structures <br />
query.py - records audio to be recognized <br />
search.py - searches the recorded query audio in the database <br />

Additional libraries used: numpy, matplotlib, librosa, scipy, wave, pyaudio
