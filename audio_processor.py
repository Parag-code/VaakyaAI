import speech_recognition as sr
import tempfile

def transcribe_audio(audio_file, language="en"):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name
    with sr.AudioFile(tmp_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        text = "Could not understand audio."
    except sr.RequestError as e:
        text = f"Could not request results; {e}"
    return text