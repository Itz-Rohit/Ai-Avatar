from gtts import gTTS
import os

text = "नमस्ते, आप कैसे हैं?"
tts = gTTS(text=text, lang="hi")
tts.save("output.mp3")
os.system("start output.mp3")  # For Windows, use "afplay output.mp3" on macOS.
