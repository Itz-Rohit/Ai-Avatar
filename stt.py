import os
import uuid
import tempfile
import whisper
import subprocess
import time

def convert_to_wav(input_file, output_file):
    """
    Convert any audio format (MP3, M4A, WAV) to a 16-bit WAV mono file at 16kHz using ffmpeg.
    """
    try:
        print(f"[DEBUG] Converting {input_file} to {output_file} using ffmpeg...")
        subprocess.run([
            "ffmpeg", "-i", input_file, "-ac", "1", "-ar", "16000", "-sample_fmt", "s16", output_file, "-y"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[DEBUG] Conversion successful: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error converting audio to WAV: {e}")

def transcribe_audio_file(audio_file, language="hi"):
    """
    Convert an uploaded Hindi audio file into text using OpenAI Whisper.
    """
    try:
        # Generate a unique temporary file path
        temp_audio_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp3")  # Save as MP3 first

        # Read and save the uploaded file
        data = audio_file.read()
        if not data:
            raise Exception("No audio data received.")

        with open(temp_audio_path, "wb") as f:
            f.write(data)

        print(f"[DEBUG] Temporary audio file created: {temp_audio_path}")

        # Ensure file exists before conversion
        time.sleep(1)
        if not os.path.exists(temp_audio_path):
            raise Exception(f"[ERROR] File does not exist after writing: {temp_audio_path}")

        # Convert to proper WAV format before processing
        converted_audio_path = temp_audio_path.replace(".mp3", ".wav")
        convert_to_wav(temp_audio_path, converted_audio_path)

        print(f"[DEBUG] Converted audio file: {converted_audio_path}")

        # Load Whisper model
        model = whisper.load_model("large-v1")

        # Transcribe the converted WAV audio
        result = model.transcribe(converted_audio_path, language=language)

        # Clean up temp files
        os.remove(temp_audio_path)
        os.remove(converted_audio_path)
        print(f"[DEBUG] Temp files deleted.")

        return result["text"]

    except Exception as e:
        raise Exception(f"Error transcribing audio: {e}")
