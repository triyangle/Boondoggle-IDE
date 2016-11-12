#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from text2code import *

class CustomRecognizer(sr.Recognizer):
    def recognize_google(self, audio_data, key = None, language = "en-US", show_all = False):
            """
            Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the Google Speech Recognition API.
            The Google Speech Recognition API key is specified by ``key``. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it **may be revoked by Google at any time**.
            To obtain your own API key, simply following the steps on the `API Keys <http://www.chromium.org/developers/how-tos/api-keys>`__ page at the Chromium Developers site. In the Google Developers Console, Google Speech Recognition is listed as "Speech API".
            The recognition language is determined by ``language``, an RFC5646 language tag like ``"en-US"`` (US English) or ``"fr-FR"`` (International French), defaulting to US English. A list of supported language values can be found in this `StackOverflow answer <http://stackoverflow.com/a/14302134>`__.
            Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the raw API response as a JSON dictionary.
            Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
            """
            assert isinstance(audio_data, sr.AudioData), "`audio_data` must be audio data"
            assert key is None or isinstance(key, str), "`key` must be `None` or a string"
            assert isinstance(language, str), "`language` must be a string"

            flac_data = audio_data.get_flac_data(
                convert_rate = None if audio_data.sample_rate >= 8000 else 8000, # audio samples must be at least 8 kHz
                convert_width = 2 # audio samples must be 16-bit
            )
            if key is None: key = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
            phrases = ["variable " + chr(char) for char in range(ord("A"), ord("Z") + 1)]
            phrases.extend(["variable " + chr(char) for char in range(ord("a"), ord("z") + 1)])
            url = "http://www.google.com/speech-api/v2/recognize?{0}".format(sr.urlencode({
                "client": "chromium",
                "lang": language,
                "key": key,
                "speech_context": {
                    "phrases": str(phrases)
                    }
            }))
            request = sr.Request(url, data = flac_data, headers = {"Content-Type": "audio/x-flac; rate={0}".format(audio_data.sample_rate), "speech_context": str(phrases)})

            # obtain audio transcription results
            try:
                response = sr.urlopen(request, timeout=None)
            except sr.HTTPError as e:
                raise sr.RequestError("recognition request failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code)))) # use getattr to be compatible with Python 2.6
            except sr.URLError as e:
                raise sr.RequestError("recognition connection failed: {0}".format(e.reason))
            response_text = response.read().decode("utf-8")

            # ignore any blank blocks
            actual_result = []
            for line in response_text.split("\n"):
                if not line: continue
                result = sr.json.loads(line)["result"]
                if len(result) != 0:
                    actual_result = result[0]
                    break

            # return results
            if show_all: return actual_result
            if "alternative" not in actual_result: raise sr.UnknownValueError()
            for entry in actual_result["alternative"]:
                if "transcript" in entry:
                    return entry["transcript"]
            raise sr.UnknownValueError() # no transcriptions available

# obtain audio from the microphone
r = CustomRecognizer()
while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something!")
        audio = r.listen(source)

# recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        raw_result = r.recognize_google(audio, key = "AIzaSyCFeldgQ8Pf-qv0dn-ztbpuZjUMC9i380w")
        print("Google Speech Recognition thinks you said " + raw_result)
#        gui(convert_to_code(raw_result))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
