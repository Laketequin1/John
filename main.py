from perplexity import Perplexity
import speech_recognition as sr
import pyttsx3
import re
import multiprocessing
import threading
import time
import random
from pocketsphinx import LiveSpeech
import sys

precursor = "hey john "
thinking_options = ["Thinking", "Let me think", "Accessing database", "Just a second", "Searching for information", "Processing your request", "Considering responses", "Gathering information", "Finding results"]

def check_stop():
    speech = LiveSpeech()
    for word in speech:
        if "stop" in str(word):
            print("Stop said!")
            sys.exit()

def speak(message):
    # Windows says message
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def remove_square_bracket(input_string):
    # Remove '[number]' from a string
    result = re.sub(r'\[\d+\]', '', input_string)
    return result

def remove_precursor(input_string):
    # Removes all text before precursor, as well as the precursor
    index = input_string.index(precursor)
    return input_string[index:].replace(precursor, "")

def main():
    r = sr.Recognizer()
    perplexity = Perplexity()

    p1 = None
    p2 = None
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)

                print("Listening...")
                audio = r.listen(source)

                capture = r.recognize_google(audio, ).lower()
                print("You asked:", capture)

                if precursor in capture:
                    capture = remove_precursor(capture)

                    p1 = multiprocessing.Process(target=speak, args=(random.choice(thinking_options),))
                    p1.start()

                    answer = list(perplexity.search(capture))
                    result = remove_square_bracket(answer[-1]['answer'])
                    
                    p2 = multiprocessing.Process(target=speak, args=(result,))
                    p2.start()
                    
                    t = threading.Thread(target=check_stop)
                    t.start()

                    while p2.is_alive():
                        if not t.is_alive():
                            p2.terminate()
                        time.sleep(0.05)

                    if t.is_alive():
                        t.join()

        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))

        except sr.UnknownValueError:
            print("No text captured")

if __name__ == "__main__":
    main()