from backend.ml_logic.preprocessor import preprocess_data
from backend.ml_logic.postprocessor import postprocess_prediction
from backend.ml_logic.encoder import encode_data
from backend.ml_logic.model import load_model
from backend.main import predict_with_pop2piano
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, UploadFile
import zipfile
import io
import os
import shutil

app = FastAPI()
temp_data_folder = "backend/temp_data"


@app.get("/")
def some_function():
    print("Hello!")


# Get prediction
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

@app.post("/predict-progressive/")
async def predict(file: UploadFile):
    try:
        file_path = os.path.join(temp_data_folder, "guitar.mid")
        zipped_path = os.path.join(temp_data_folder, "drum_files.zip")

        with open(file_path, "wb") as midi_file:
            shutil.copyfileobj(file.file, midi_file)
        output = predict_with_pop2piano(file_path)

        with zipfile.ZipFile(zipped_path, 'w',
                     compression=zipfile.ZIP_DEFLATED,
                     compresslevel=9) as zf:
            zf.write(output["midi"], "drums.mid")
            zf.write(output["wav"], "drums.wav")
            zf.write(output["wav_combined"], "guitar_drums_combined.wav")

        return FileResponse(zipped_path)

    except ValueError as e:
        # Return error response if something goes wrong
        return JSONResponse(content={"error": str(e)}, status_code=500)
