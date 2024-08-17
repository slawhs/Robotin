import speech_recognition as sr
import pyttsx3

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=7)
    try:
        return r.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        return "Puedes repetirlo, por favor?"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)
    
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        text = listen()
        print("You said: ", text)
        speak(text)
        if text == "exit":
            break


