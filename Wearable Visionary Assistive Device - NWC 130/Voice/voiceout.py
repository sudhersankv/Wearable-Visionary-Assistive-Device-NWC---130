import pyttsx3

engine = pyttsx3.init()

def VO(myText):


    # Get a list of available voices
    voices = engine.getProperty('voices')

    # Select a male voice (you might need to adjust the index based on your system)
    for voice in voices:
        if voice.gender == 'male':  # Assuming 'male' is a valid value
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 140)

            break  # Stop after finding a male voice

    # Speak the text
    engine.say(myText)
    engine.runAndWait()

