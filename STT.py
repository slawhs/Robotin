# pip3 install speechrecognition
# pip3 install pyaudio

import speech_recognition as sr
import pyttsx3

# INTENTO 1 -----------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=7)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
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



# INTENTO 2 -----------------------------
# r = sr.Recognizer()

# def record_text():
#     while(1):
#         try:
#             with sr.Microphone() as source2:
#                 r.adjust_for_ambient_noise(source2, duration=0.2)
#                 print("Say something!")
#                 audio2 = r.listen(source2, timeout=10, phrase_time_limit=5)
#                 MyText = r.recognize_google(audio2)
#                 return MyText
            
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))

#         except sr.UnknownValueError:
#             print("unknown error occured")
#             return "Could not understand audio"
        
#     return

# def output_text(text):
#     f = open("output.txt", "a")
#     f.write(text + "\n")
#     f.close()
#     return

# while(1):
#     text = record_text()
#     print("You said: ", text)
#     output_text(text)
#     if text == "exit":
#         break