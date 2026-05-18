import whisper
import os
os.environ["PATH"] += os.pathsep + r'C:\ffmpeg\bin'

model = whisper.load_model("base")

def listen(filename="input.wav"):
    result = model.transcribe(filename, language="ru", fp16=False)
    return result["text"]