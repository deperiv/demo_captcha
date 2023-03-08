from pydub import AudioSegment
import os
import tempfile

import speech_recognition as sr

ret = None
tmp_dir = tempfile.gettempdir()
mp3_file = os.path.join(tmp_dir, r"C:\Users\DANIEL\Desktop\ITSENSE\demo_captcha\webscrapping\tools\audio.mp3")
wav_file = os.path.join(tmp_dir, r"C:\Users\DANIEL\Desktop\ITSENSE\demo_captcha\webscrapping\tools\audio.wav")
tmp_files = [mp3_file, wav_file]

AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

recognizer = sr.Recognizer()

with sr.AudioFile(wav_file) as source:
    recorded_audio = recognizer.listen(source)
    text = recognizer.recognize_google(recorded_audio)

print(text)