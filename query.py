import pyaudio
import wave
import librosa as lr

#####################################################################
# recordaudio
# Record query audio to search in the database.
# --- Outputs ---
# T - recorded audio samples
#####################################################################
def recordaudio():
    # set up parameters for recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 8
    WAVE_OUTPUT_FILENAME = "recording.wav"

    # open stream for recording
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording *")

    # recording frame by frame and appending
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording *")

    # end recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # open file for writing
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # load file and resample to 8192 Hz
    x, fs = lr.load('recording.wav', sr = 8192, mono = True)

    return x
