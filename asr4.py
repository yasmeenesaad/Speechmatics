import asyncio
from flask import Flask, request, jsonify
from speechmatics.batch import AsyncClient, TranscriptionConfig
import os

app = Flask(__name__)

API_KEY = "Y1hMSnuxPug5IRHQ0kdZDEzlUpxRxIc4"

# Speechmatics config
config = TranscriptionConfig(
    language="ar",
    diarization="speaker",
    additional_vocab=[
        {"content": "باقة"},
        {"content": "روومنج"},
        {"content": "اي دي اس ال"},
        {"content": "فليكس"}
    ]
)

# Async transcription function
async def transcribe_audio(file_path):
    client = AsyncClient(api_key=API_KEY)

    result = await client.transcribe(
        audio_file=file_path,
        transcription_config=config
    )

    await client.close()
    return result.transcript_text


# API endpoint
@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Save file temporarily
    file_path = f"temp_{file.filename}"
    file.save(file_path)

    try:
        # Run async function inside Flask
        transcript = asyncio.run(transcribe_audio(file_path))

        return jsonify({
            "transcript": transcript
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    app.run(debug=True)
    