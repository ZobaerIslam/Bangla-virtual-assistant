# Import essential module for this project
import googletrans
import speech_recognition as sr
import gtts
import playsound


# google speech recognition supported languages link is below:
# https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt-tts
input_lang = 'bn-IN'
destination_lang = 'bn'

# Create instances
try:
    recognizer = sr.Recognizer()
    translator = googletrans.Translator()
except Exception as e:
    print("Exception:", e)


# Take command from speech
def take_command():
    with sr.Microphone() as source:
        print("Listening, Speak now...")
        voice = recognizer.listen(source)
        text = ''
        try:
            text = recognizer.recognize_google(voice, language=input_lang)
            print(text)
        except Exception as ex:
            print('Exception:', ex)

    return text


def translate():
    text = take_command()
    translated = translator.translate(text, dest=destination_lang)
    converted_audio = gtts.gTTS(translated.text, lang=destination_lang)
    converted_audio.save('speak.mp3')
    playsound.playsound('speak.mp3')


translate()
