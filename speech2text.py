#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from text2code import *

# obtain audio from the microphone
class Speech2Text:
    def __init__(self):
        self.r = sr.Recognizer()
    def process(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print("Say something!")
            self.audio = self.r.listen(source)

            # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            raw_result =  self.r.recognize_google(self.audio, show_all=True)
            print("Google Speech Recognition thinks you said " + str(raw_result))
            #        gui(convert_to_code(raw_result))
            word_array = text2arr(raw_result)
            word_array = fixtxterror(word_array)
            return expression(word_array)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
