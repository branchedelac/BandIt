# TODO Add all functions related to preprocessing here

import pretty_midi
import numpy as np
import os
import IPython

# import fluidsynth
import glob
import pandas as pd
import logging
from tokenizers import Tokenizer

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def preprocess_data():
    data_path = "data"
    song_list = glob.glob(os.path.join(data_path, "*.mid"))[:20]
    logging.info("Found %s midifiles in folder %s", str(len(song_list)), data_path)
    logging.info("Processing songs...")
    for idx, song_path in enumerate(song_list):
        if idx % 10 == 0:
            logging.info("Number of songs processed: %s", idx)

        # Normalize tempo
        normalized_midi, song_title = bpm_to_120(song_path)

        # Extract guitar and drum
        gd_track_dict = extract_guitar_and_drums(normalized_midi, song_title)

        # Split track into bars
        gd_bars_dict = tracks_to_bars(gd_track_dict)

        # Standardize bar start time
        guitar_bars_standard = standardize_bars(
            gd_bars_dict["guitar_bars"], gd_bars_dict["down_beats"]
        )
        drum_bars_standard = standardize_bars(
            gd_bars_dict["drum_bars"], gd_bars_dict["down_beats"]
        )

        # Turn bar objects into strings
        guitar_bars_string = [
            objects_to_strings(bar) for bar in guitar_bars_standard
        ]
        drum_bars_string = [
            objects_to_strings(bar) for bar in guitar_bars_standard
        ]

        # Encode using pretrained vocab
        #encoded_guitars = drum_encoder(guitar_bars_string)
        #encoded_drums = drum_encoder(drum_bars_string)

        print(guitar_bars_string)
        print(guitar_bars_string)

# Normalize tempo
def bpm_to_120(midi_file):
    """
    This function evens out the tempo throuout the song to be 120 BPM,
    even if there are tempo changes. It gets a midi file as an input
    and outputs a modified pretty_midi object and the song title as a string.
    """

    mid = pretty_midi.PrettyMIDI(midi_file)

    tempo = mid.get_tempo_changes()
    num_of_changes = len(tempo[0])
    full_length = mid.get_end_time()

    old_times = []
    changes = [0]

    for i in range(num_of_changes):
        old_times.append(tempo[0][i])
        if i < (num_of_changes - 1):
            changes.append((tempo[0][i + 1] - tempo[0][i]) * (tempo[1][i] / 120))
        else:
            changes.append((full_length - tempo[0][i]) * (tempo[1][i] / 120))

    old_times.append(full_length)
    new_times = np.cumsum(changes)

    mid.adjust_times(old_times, new_times)

    song_title = os.path.splitext(os.path.basename(midi_file))[0]

    return mid, song_title


# TODO Extract guitar and drum
def extract_guitar_and_drums(mid, song_title="unknown"):
    """This function extracts the guitar and drum tracks from a midi file.
    The first input is either a path to a midi file (for example: 'raw_data/song_name.mid')
    in string format, or a pretty_midi object. The second input is the song title as a string.
    The output is a dictionary with the song name, guitar track and drum track"""

    if type(mid) == str:
        mid = pretty_midi.PrettyMIDI(mid)
        song_title = os.path.splitext(os.path.basename(mid))[0]

    guitars = []
    lengths_guitar = []
    drums = []
    lengths_drums = []

    for instrument in mid.instruments:
        if instrument.is_drum:
            drums.append(instrument)
            lengths_drums.append(len(instrument.notes))

        if (instrument.program >= 24) and (instrument.program <= 31):
            guitars.append(instrument)
            lengths_guitar.append(len(instrument.notes))

    drum_track = drums[lengths_drums.index(max(lengths_drums))]
    guitar_track = guitars[lengths_guitar.index(max(lengths_guitar))]

    song_dict = {
        "title": song_title,
        "down_beats": mid.get_downbeats(),
        "guitar": guitar_track,
        "drums": drum_track,
    }
    return song_dict


# Split track into bars
def tracks_to_bars(song_dict: dict) -> dict:
    """This function accepts a dictionary as an input with 4 keys: 'title', 'down_beats', 'guitar', 'drums'.
    The function takes the guitar and drums, both pretty_midi instrument objects, and cuts them up into a sequence of individual bars.
    The output is a dictionary that contains the following keys/values: song_title, a list of guitar bars, a list of drum bars, and a list of the song's downbeats
    """

    new_dict = {}
    new_dict["song_title"] = song_dict["title"]
    guitar = song_dict["guitar"]
    drums = song_dict["drums"]
    down_beats_array = song_dict["down_beats"]

    guitar_bars_list = []
    drums_bars_list = []

    for i in range(len(down_beats_array)):
        if i < len(down_beats_array) - 1:
            end_time = down_beats_array[i + 1]
        else:
            end_time = down_beats_array[i] + 2

        guitar_bar = []
        drums_bar = []
        for j in range(len(guitar.notes)):
            if (guitar.notes[j].start >= down_beats_array[i]) and (
                guitar.notes[j].end < end_time
            ):
                guitar_bar.append(guitar.notes[j])

        for k in range(len(drums.notes)):
            if (drums.notes[k].start >= down_beats_array[i]) and (
                drums.notes[k].end < end_time
            ):
                drums_bar.append(drums.notes[k])

        drums_bars_list.append(drums_bar)
        guitar_bars_list.append(guitar_bar)

    new_dict["guitar_bars"] = guitar_bars_list
    new_dict["drum_bars"] = drums_bars_list
    new_dict["down_beats"] = down_beats_array.tolist()
    return new_dict


# Standardize bar start time
def standardize_bars(list_of_bars, downbeats):
    """
    This function standardizes the timing of musical bars
    so that each bar will start at the same time point.
    It gets a list of bars and the list of downbeats as inputs
    and returns a list of bars that all start with time = 1
    """
    std_bars = list_of_bars.copy()
    for i in range(len(list_of_bars)):
        for j in range(len(list_of_bars[i])):
            if i == 0:
                std_bars[0][j].start = std_bars[0][j].start / downbeats[1]
                std_bars[0][j].end = std_bars[0][j].end / downbeats[1]
            else:
                std_bars[i][j].start = std_bars[i][j].start / downbeats[i]
                std_bars[i][j].end = std_bars[i][j].end / downbeats[i]

    return std_bars


# Turn bar objects into strings
def objects_to_strings(list_of_bars):
    """
    This Function takes bars that are note objects and
    converts them to strings for the purpose of tokenization
    """
    list_of_strings = [str(bar) for bar in list_of_bars]
    return list_of_strings

def guitar_encoder(guitar_track):
    """
    This function tokenizes a guitar track based on a pre trained guitar tokenizer.
    The input is a list of strings of guitar bars, the output is a list of
    corresponding tokens
    """

    guitar_tokenizer = Tokenizer.from_file("guitar_tokenizer.json")
    encoded_guitar = []
    for bar in guitar_track:
        if str(bar) in list(guitar_tokenizer.get_vocab().keys()):
            encoded_guitar.append(guitar_tokenizer.get_vocab()[bar])
        else:
            encoded_guitar.append("[UNK]")
    return encoded_guitar


def drum_encoder(drum_track):
    """
    This function tokenizes a drum track based on a pre trained drums tokenizer.
    The input is a list of strings of drum bars, the output is a list of
    corresponding tokens
    """

    drum_tokenizer = Tokenizer.from_file("drum_tokenizer.json")
    encoded_drum = []
    for bar in drum_track:
        if str(bar) in list(drum_tokenizer.get_vocab().keys()):
            encoded_drum.append(drum_tokenizer.get_vocab()[bar])
        else:
            encoded_drum.append("[UNK]")

    return encoded_drum


preprocess_data()
