import asyncio
from speechmatics.batch import AsyncClient, TranscriptionConfig

API_KEY = "Y1hMSnuxPug5IRHQ0kdZDEzlUpxRxIc4"
AUDIO_FILE= "C:/Users/jasmine/Downloads/speechmatics/examples_nodejs_example.wav"

config = TranscriptionConfig(
    language = "en",
    diarization="speaker"
)

async def main():
    client = AsyncClient(api_key=API_KEY)
    result = await client.transcribe(
        audio_file=AUDIO_FILE, 
        transcription_config=config
    )
    print(result.transcript_text)
    await client.close()

asyncio.run(main())