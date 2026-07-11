import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

def listen():
    sample_rate = 44100
    duration = 25

    print("🎤 Speak now (25 seconds)...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    write("recording.wav", sample_rate, recording)

    recognizer = sr.Recognizer()

    with sr.AudioFile("recording.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except sr.RequestError as e:
        print("Speech Recognition Error:", e)
        return ""