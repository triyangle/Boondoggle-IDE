#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from text2code import *

# obtain audio from the microphone
class MyException(Exception):
    pass
class Speech2Text:

    def __init__(self, escapes):
        global ESCAPES
        self.r = sr.Recognizer()
        self.Joe = True
        self.escapes = escapes
        ESCAPES = escapes


    def process(self, autocorrect):
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
            print('allahu akbar!!!')

            #raw_result is now a list of dictionaries of results
            if not raw_result:
                raise sr.UnknownValueError
            raw_result = raw_result['alternative']
            results = [op['transcript'] for op in raw_result]
            self.result = results[0]

            if autocorrect:
                for r in results[1:]:
                    if self.result in r and len(r.replace(self.result,""))==2 and len(r.replace(self.result,"").strip())==1:
                        self.result = r

            self.result = self.result.lower()

            print("Google Speech Recognition thinks you said " + self.result + str(raw_result))
            
            return convertstring(self.result, autocorrect)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

def convertstring(result, autocorrect = False):
    result = result.lower()
    word_array = text2arr(result)
    word_array = fixtxterror(word_array) if autocorrect else word_array

    if word_array[0].lower() == 'boondoggle' or word_array[0].lower() == 'boondoggles':
        if word_array[1] in ESCAPES:
            ESCAPES[word_array[1]](*(word_array[2:]))
            return ""
        return "<bad escape sequence>"
    else:
        return expression(word_array)[0]
