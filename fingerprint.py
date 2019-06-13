import librosa as lr
import numpy as np
import matplotlib.pyplot as plt
import scipy

#####################################################################
# createfingerprint
# Creates a simple fingerprint, which is essentially a scatter plot
# of spectrogram peaks on a matrix
# --- Inputs ---
# x - Time domain audio clip samples
# --- Outputs ---
# output - fingerprint matrix
#####################################################################
def createfingerprint(x, plot = False):
    # generate spectrogram and convert to log scale
    X = lr.stft(x, n_fft = 1024, hop_length = 32, window = "blackman")
    X = np.abs(X)
    L, W = np.shape(X)

    # extract peaks and use max filter to select highest peak in the neighbourhood
    output = peakextract(X)
    output = scipy.ndimage.maximum_filter(output, size = 25)
    max_peak = np.max(output)
    output = np.where(output == 0 , -1 , output)
    output = np.where(X == output, 1, 0)

    # Display fingerprint with original spectrogram if enabled
    if plot:
        plt.imshow(X)
        y_ind, x_ind = np.where(output != 0)
        plt.scatter(x = x_ind, y = y_ind, c = 'r', s = 8.0)
        plt.gca().invert_yaxis()
        plt.xlabel('Frames')
        plt.ylabel('Bins')
        plt.draw()

    return output

#####################################################################
# peakextract
# Extracts peaks from every time frame in the spectrogram
# --- Inputs ---
# S - Spectrogram
# --- Outputs ---
# peaks - Matrix with peaks extracted from each band
#####################################################################
def peakextract(S):
    # initialise peaks matrix
    row, col = np.shape(S)
    peaks = np.zeros((row, col))

    # split frequency spectrum into logarithmic bands
    bands = np.array([[1, 11], [12, 21], [22, 41], [42, 81], [82, 161], [162, 513]])

    # find maximum in each frame in each band and update the peaks matrix
    for i in range(col):
        for j in range(6):
            q1 = bands[j, 0]
            q2 = bands[j, 1]
            frame_band = S[q1:q2, i]
            localpeak = np.max(frame_band)
            index = np.where(frame_band == localpeak)
            peaks[q1 + index[0], i] = localpeak

    return peaks

#####################################################################
# createhashes
# Create hashes from peaks matrix and store then in a table. A hash is
# made from a time-frequency pair in the peaks matrix.
# --- Inputs ---
# peaks - binary matrix with peak locations set to 1
# offset - frame number for an anchor point on the server side
# --- Outputs ---
# T - hash table
# O - offset (only for server side)
#####################################################################
def createhashes(peaks, offset = False):
    # transpose so frames are in order
    peaks = np.transpose(peaks)
    # find locations of peaks and cound the number of peaks
    points = np.where(peaks != 0)
    num_points = np.shape(points[0])[0]

    # create empty list containing empty lists with index 0-512
    T = [ [] for i in range(513) ]

    # only do on the server side
    if offset:
        O = [ [] for i in range(513) ]

    # update hash table
    for i in range(num_points):
        for j in range(num_points - i):
            # if frame is delta time is between 1-50 then make float with f1.delta_t and append to list
            if abs(points[0][i] - points[0][i+j]) != 0 and abs(points[0][i] - points[0][i+j]) < 51:
                if abs(points[0][i] - points[0][i+j]) < 10:
                    T[points[1][i]].append(float(str(points[1][i+j]) + '.0' + \
                    str(abs(points[0][i] - points[0][i+j]))))
                else:
                    T[points[1][i]].append(float(str(points[1][i+j]) + '.' + \
                    str(abs(points[0][i] - points[0][i+j]))))

                # only do on the server side
                if offset:
                    O[points[1][i]].append(points[0][i])

    # server side
    if offset:
        return T, O
    # client side
    else:
        return T
