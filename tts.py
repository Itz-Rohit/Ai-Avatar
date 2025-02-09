import os
import subprocess
from gtts import gTTS

def text_to_speech(text, output_file="static/generated/output.mp3"):
    """
    Converts text to speech and saves it as an MP3 file.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tts = gTTS(text=text, lang="hi")
        tts.save(output_file)

        if not os.path.exists(output_file):
            raise FileNotFoundError(f"TTS output file not found: {output_file}")

        print(f"[SUCCESS] Speech generated: {output_file}")
        return output_file  # Return the MP3 file path
    except Exception as e:
        raise Exception(f"Error generating speech: {e}")
