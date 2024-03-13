import os
import glob
import pretty_midi
from midi2audio import FluidSynth
import librosa

import numpy as np
import pandas as pd
from transformers import Pop2PianoForConditionalGeneration, Pop2PianoProcessor

temp_data_folder = "backend/temp_data"


def preprocess():
    print("Gonna get preprocessing now! Heja heja!")


def train():
    print("Gonna get training now! Woohoo!")


def evaluate():
    print("Gonna get evaluating now! Fingers crossed!")


def predict_with_pop2piano(midi_path):
    """Given a midi as a BytesIO object, returns a PrettyMIDI object with a drum arrangement."""

    # Load model
    model = Pop2PianoForConditionalGeneration.from_pretrained("sweetcocoa/pop2piano")
    processor = Pop2PianoProcessor.from_pretrained("sweetcocoa/pop2piano")

    # Define paths for temporary storage
    temp_wav_path = os.path.join(temp_data_folder, "guitar.wav")

    # Save midi as wav to use with model
    fs = FluidSynth()
    fs.midi_to_audio(midi_path, temp_wav_path)

    # Load wav
    audio, sr = librosa.load(
        temp_wav_path, sr=44100
    )

    # Preprocess audio
    inputs = processor(audio=audio, sampling_rate=sr, return_tensors="pt")

    # Predict
    model_output = model.generate(
        input_features=inputs["input_features"], composer="composer1"
    )

    # Post-process audio
    tokenizer_output = processor.batch_decode(
        token_ids=model_output, feature_extractor_output=inputs
    )["pretty_midi_objects"][0]

    tokenizer_output.instruments[0].is_drum = True

    # Save new drums as midi
    tokenizer_output.write(os.path.join(temp_data_folder, f"drums.mid"))
    # Save drums as wav
    fs.midi_to_audio(
        os.path.join(temp_data_folder, "drums.mid"),
        os.path.join(temp_data_folder, "drums.wav"),
    )

    return tokenizer_output


if __name__ == "__main__":
    print("heeey")
