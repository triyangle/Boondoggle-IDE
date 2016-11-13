#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from text2code import *

# obtain audio from the microphone
class MyException(Exception):
    pass
class Speech2Text:

    def __init__(self, escapes):
        self.r = sr.Recognizer()
        self.Joe = True
        self.escapes = escapes
    def process(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print("Say something!")
            audio = self.r.listen(source)
            if not self.Joe:
                raise MyException
            # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            raw_result =  self.r.recognize_google(audio, show_all=True)

            #raw_result is now a list of dictionaries of results
            if not raw_result:
                raise sr.UnknownValueError
            raw_result = raw_result['alternative']
            results = [op['transcript'] for op in raw_result]
            self.result = results[0]
            for r in results[1:]:
                if results[0] in r and len(r.replace(results[0],""))==2 and len(r.replace(results[0],"").strip())==1:
                    self.result = r

            print("Google Speech Recognition thinks you said " + self.result + str(raw_result))
            self.result = self.result.lower()
            word_array = text2arr(self.result)
            word_array = fixtxterror(word_array)

            if word_array[0] == 'boondoggle':
                return self.escapes[word_array[1]]
            else:
                return expression(word_array)[0]

        except sr.UnknownValueError or MyException:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""
