
import numpy as np
import matplotlib.pyplot as plt

#####################################################################
# comparetables
# Compares the hash table fingerprint to the ones present in the
# database and returns the number of matches
# --- Inputs ---
# table - hash table (fingerprint of the query)
# --- Outputs ---
# matched_pairs_list - number of matches against each song in the
#                      database
#####################################################################

def comparetables(table):
    # load the database
    npzfile1 = np.load('server_tables.npz')
    npzfile2 = np.load('offset_times.npz')
    database = npzfile1['arr_0']
    offset_times = npzfile2['arr_0']

    matched_pairs_list = np.zeros((len(database), 1))
    hist_list = np.zeros((len(database), 1))

    # calculate the number of matches against each fingerprint in the
    # database
    for h in range(len(database)):
        matched_pairs = 0
        add_to_hist = []
        for i in range(513):
            # search only if list is not empty
            if table[i]:
                for j in table[i]:
                    # increment the count if pair is found on the list
                    if j in database[h][i]:
                        indices = [i for i, x in enumerate(database[h][i]) if x == j]
                        matched_pairs = matched_pairs + len(indices)
                        # fetch offset times for all matches
                        for o in indices:
                            add_to_hist.append(offset_times[h][i][o])
        matched_pairs_list[h] = matched_pairs
        # fetch max value of histogram
        if add_to_hist:
            maxh = np.max(add_to_hist)
            hist, edges = np.histogram(add_to_hist, bins = range(0, (maxh + (maxh + 1) % 2050), 2050))
            hist_list[h] = np.max(hist)

    return matched_pairs_list, hist_list

#####################################################################
# fetchID
# Performs comparison and searches for the song with most number of
# matches.
# --- Inputs ---
# fprint - Hash table (fingerprint of the query)
# --- Outputs ---
# output - Song name
#####################################################################
def fetchID(fprint):
    # find matches against each fingerprint on the server and compute
    # the ratios
    matched_pairs, hists = comparetables(fprint)
    num_pairs = sum(map(len, fprint))
    ratios = matched_pairs / num_pairs

    # find maximum of the matches and update the index
    max_match = np.max(ratios)
    max_hist = np.max(hists)

    # finding index for song maximum number of matches and maximum value
    # in histogram
    id_value = np.where(ratios == max_match)
    id_hist = np.where(hists == max_hist)

    # if the ID is same for both, song is in database
    if id_value == id_hist:
        id = id_value
    else:
        id = -1

    # look up the song name for that index
    all_names = np.load('song_names.npz')
    if id == -1:
        name = "Not found!"
    else:
        name = all_names['arr_0'][id[0][0]]
    #
    print('Number of Matches\t' + 'Ratio\t\t' + 'Hist max\t\t' 'Song Name')
    for i in range(10):
        print(str(matched_pairs[i][0]) + '\t\t\t' + \
        '%0.4f' % (ratios[i][0]) + '\t\t' + '%0.4f' % hists[i] + '\t\t' + \
        str(all_names['arr_0'][i]))

    return name
