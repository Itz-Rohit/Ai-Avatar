from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import subprocess

from stt import transcribe_audio_file
from llm import generate_response
from tts import text_to_speech
from avatar_sync import create_avatar_animation

app = FastAPI(title="Hindi Audio Processing API", version="1.0")

# Mount the static directory to serve HTML, CSS, JS, and generated files.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure the generated folder exists
os.makedirs("static/generated", exist_ok=True)

# Root endpoint to serve the front-end page.
@app.get("/", response_class=HTMLResponse)
def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/process_audio/")
async def process_audio(audio: UploadFile, language: str = Form("hi")):
    try:
        # Step 1: Save Uploaded Audio
        input_audio_path = "static/generated/input_audio.wav"
        with open(input_audio_path, "wb") as f:
            f.write(audio.file.read())
        print("[DEBUG] Audio file saved:", input_audio_path)

        # Step 2: Speech-to-Text (STT) (Fixed - Open file in binary mode)
        with open(input_audio_path, "rb") as audio_file:
            transcription = transcribe_audio_file(audio_file, language)
        print("[DEBUG] Transcription:", transcription)

        # Step 3: AI Response (LLM)
        ai_response = generate_response(transcription)
        print("[DEBUG] AI Response:", ai_response)

        # Save AI response as a text file
        ai_response_path = "static/generated/ai_response.txt"
        with open(ai_response_path, "w", encoding="utf-8") as f:
            f.write(ai_response)

        # Step 4: Text-to-Speech (TTS)
        tts_output_mp3 = "static/generated/output.mp3"
        tts_output_wav = "static/generated/output.wav"  # WAV for avatar animation

        text_to_speech(ai_response, output_file=tts_output_mp3)

        # Ensure the TTS MP3 file was generated
        if not os.path.exists(tts_output_mp3):
            raise FileNotFoundError(f"[ERROR] TTS did not generate a valid audio file at {tts_output_mp3}")

        print("[DEBUG] Audio generated:", tts_output_mp3)

        # Convert MP3 to WAV before passing to avatar animation
        print("[INFO] Converting MP3 to WAV for avatar animation...")
        convert_command = f'ffmpeg -y -i "{tts_output_mp3}" -ar 24000 -ac 1 -c:a pcm_s16le "{tts_output_wav}"'
        subprocess.run(convert_command, shell=True, check=True)

        if not os.path.exists(tts_output_wav):
            raise FileNotFoundError(f"[ERROR] WAV conversion failed: {tts_output_wav}")

        print("[SUCCESS] MP3 converted to WAV:", tts_output_wav)

        # Step 5: Avatar Animation (Using OpenCV Emoji Animation)
        final_video_path = "static/generated/final_output.mp4"
        create_avatar_animation(tts_output_wav, output_video=final_video_path)

        # Ensure the animation file was created
        if not os.path.exists(final_video_path):
            raise FileNotFoundError(f"[ERROR] Avatar animation failed; no video found at {final_video_path}")

        print("[DEBUG] Avatar animation generated:", final_video_path)

        return JSONResponse(content={
            "transcription": transcription,
            "ai_response": ai_response,
            "audio_file": f"/static/generated/output.mp3",
            "avatar_video": f"/static/generated/final_output.mp4"
        })

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
