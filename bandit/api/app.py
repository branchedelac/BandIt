from bandit.ml_logic.preprocessor import preprocess_data
from bandit.ml_logic.postprocessor import postprocess_prediction
from bandit.ml_logic.encoder import encode_data
from bandit.ml_logic.model import load_model
from pretty_midi import PrettyMIDI

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def some_function():
    print("Hello!")

# Get prediction
# Maybe this needs to be a post given the midi input data...
#http://127.0.0.1:8000/predict?midi_file=%22cat%22
@app.post("/predict/")
async def predict(file: UploadFile):
    ### Receiving and decoding the image
    content = await file.read()
    # preprocess midi-file
    # predict with model
    # return prediction
    # postprocess midi-file to get a midi
    return f"This is my prediction for {file.filename}! Tralala!"

@app.post("/midi-to-wav")
def midi_to_wav(midi_file):
    # if we need to transform the audio into wav to play it
    # we could do this with both input and output
    return f"Listen to {midi_file} as a song! Ladidadida!"
