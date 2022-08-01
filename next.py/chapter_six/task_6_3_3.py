import pyttsx3

engine = pyttsx3.init()

engine.setProperty("volume", 0.5)

engine.say("first time i'm using a package in next.py course")

engine.runAndWait()
