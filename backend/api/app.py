from backend.ml_logic.preprocessor import preprocess_data
from backend.ml_logic.postprocessor import postprocess_prediction
from backend.ml_logic.encoder import encode_data
from backend.ml_logic.model import load_model
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile
import io

app = FastAPI()


@app.get("/")
def some_function():
    print("Hello!")


# Get prediction
# Maybe this needs to be a post given the midi input data...
# http://127.0.0.1:8000/predict?midi_file=%22cat%22
@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        ### Receiving and decoding the image
        content = await file.read()
        # Convert the bytes content into a file-like object
        midi_file_stream = io.BytesIO(content)
        # Do something with the parsed MIDI data here
        preprocess_data([midi_file_stream], [file.filename])
        return JSONResponse(content={"message": "MIDI file processed successfully"})

        # Transform the returned midi to wav and play it

    except ValueError as e:
        # Return error response if something goes wrong
        return JSONResponse(content={"error": str(e)}, status_code=500)
