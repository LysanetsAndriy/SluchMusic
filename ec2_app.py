from flask import Flask, request, jsonify
import whisper
import os
import librosa
import numpy as np
import scipy.interpolate
from scipy.signal import resample
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = whisper.load_model("base")

# Load genre classification model
genre_model = load_model('/home/ec2-user/whisper-flask/genre_classification_model.h5')

@app.route('/')
def home():
    return jsonify(
        {
            "message1": "Taranukha Pituh",
            "message2": "Taranukha Chort",
            "message3": "Taranukha Pidr"
        }
    )

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    temp_file_path = f"/tmp/{file.filename}"
    file.save(temp_file_path)

    result = model.transcribe(temp_file_path)
    lyrics = result["text"]

    os.remove(temp_file_path)  # Clean up the temporary file

    return jsonify({"lyrics": lyrics})

# Function to preprocess the audio file for genre classification
def preprocess_audio(file_path, target_sr=22050, n_mfcc=13, n_fft=2048, hop_length=512, expected_frames=130):
    # Load audio file
    signal, sr = librosa.load(file_path, sr=target_sr)
    
    # Ensure the audio is at least as long as needed to produce the expected number of frames
    min_length = hop_length * (expected_frames - 1) + n_fft
    if len(signal) < min_length:
        signal = np.pad(signal, (0, min_length - len(signal)), 'constant')
    
    # Compute MFCCs
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    
    # Ensure MFCCs have the expected number of frames
    if mfccs.shape[1] < expected_frames:
        pad_width = expected_frames - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')
    elif mfccs.shape[1] > expected_frames:
        mfccs = mfccs[:, :expected_frames]
    
    return mfccs.T

def interpolate_mfcc(mfcc, expected_frames):
    num_frames = mfcc.shape[1]
    if num_frames == expected_frames:
        return mfcc
    else:
        x = np.linspace(0, num_frames-1, num=num_frames)
        x_new = np.linspace(0, num_frames-1, num=expected_frames)
        mfcc_interpolated = np.zeros((mfcc.shape[0], expected_frames))
        for i in range(mfcc.shape[0]):
            f = scipy.interpolate.interp1d(x, mfcc[i], kind='linear')
            mfcc_interpolated[i] = f(x_new)
        return mfcc_interpolated

@app.route("/predict", methods=["POST"])
def predict_genre():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = f"/tmp/{file.filename}"
        file.save(file_path)

        # Preprocess the audio file
        mfccs = preprocess_audio(file_path)
        mfccs = mfccs[np.newaxis, ..., np.newaxis]  # Add batch and channel dimensions

        # Predict the genre
        predictions = genre_model.predict(mfccs)
        predicted_genre_index = np.argmax(predictions, axis=1)[0]
        
        genres = ["disco", "metal", "reggae", "blues", "rock", "classical", "jazz", "hiphop", "country", "pop"]
        predicted_genre = genres[predicted_genre_index]

        # Convert predictions to a list for JSON serialization
        prediction_list = predictions[0].tolist()
        prediction_dict = {genres[i]: prediction_list[i] for i in range(len(genres))}

        os.remove(file_path)  # Clean up the temporary file

        return jsonify({
            "predicted_genre": predicted_genre})


if __name__ == "__main__":
    app.run(debug=False)

