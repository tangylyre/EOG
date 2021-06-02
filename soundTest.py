# this script plays a text to speech plugin indefinitely in order to test speaker function.
# press ctrl c to exit.


from utilitiesCore import *
engine = initSpeechEngine()
while True:
    speakString("patient is in distress needs attention immediately", engine)
