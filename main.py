# Import essential module for this project
import googletrans
import speech_recognition as sr
import gtts
import playsound
import re
import random

# Google Supported voices and languages link is below:
# https://cloud.google.com/text-to-speech/docs/voices

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
            # print(text)
        except Exception as ex:
            print('Exception:', ex)

    return text


def translate(text):
    translated = translator.translate(text, dest=destination_lang)
    converted_audio = gtts.gTTS(translated.text, lang=destination_lang)
    converted_audio.save('speak.mp3')
    playsound.playsound('speak.mp3')


# Asking question
bot_template = "রোবট: {0}"
user_template = "আপনি: {0}"

# Question and Answer
responses = {
    'question': ["আমি জানি না :(",
                 "তুমি আমাকে বলো!"],
    'statement': ['আমাকে আরও বলুন!',
                  'কেন তোমার এটা মনে হল?',
                  'কতদিন ধরে তুমি এভাবে অনুভব করছো?',
                  'আমি এটি অত্যন্ত আকর্ষণীয় মনে করি',
                  'আপনি কি এটা ব্যাক আপ করতে পারেন?',
                  'কি শান্তি!',
                  ':)']}

# Extracting key phrases
rules = {'আমি চাই (.*)': ['আপনি {0} পেলে এর অর্থ কী হবে',
                          'আপনি কেন চান {0}',
                          "আপনাকে {0} পেতে কি বাধা দিচ্ছে"],
         'তোমার কি মনে আছে (.*)': ['তুমি কি ভেবেছিলে আমি ভুলে যাবো {0}',
                                   "কেন তুমি ভুলতে পারনি {0}",
                                   '{0} সম্পর্কে কি',
                                   'হ্যাঁ এবং?'],
         'আপনি কি মনে করেন (.*)': ['যদি {0}? একেবারে।',
                                   'কোন সম্ভাবনা নেই'],
         'যদি (.*)': ["আপনি কি সত্যিই মনে করেন এটি সম্ভবত {0}",
                      'আপনি কি চান যে {0}',
                      'আপনি {0} সম্পর্কে কি মনে করেন',
                      'সত্যিই--যদি {0}']}


# Define match_rules
def match_rules(rules, message):
    for pattern, responses in rules.items():
        match = re.search(pattern, message)

        if match is not None:
            response = random.choice(responses)
            var = match.group(1) if '{0}' in response else None

            return response, var

    return "default", None


# Define Response
def respond(message):
    response, phrase = match_rules(rules, message)

    if '{0}' in response:
        phrase = replace_pronouns(phrase)
        response = response.format(phrase)

    return response


# Define Replace pronouns
def replace_pronouns(message):
    message = message.lower()

    if "আমি" in message:
        return re.sub("আমি", "তুমি", message)
    if "আমার" in message:
        return re.sub("আমার", "তোমার", message)
    if "তোমার" in message:
        return re.sub("তোমার", "আমার", message)
    if "তুমি" in message:
        return re.sub("তুমি", "আমি", message)

    return message


def send_message():
    message = take_command()
    print(user_template.format(message))
    response = respond(message)
    print(bot_template.format(response))
    translate(response)


send_message()
