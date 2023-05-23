import openai
import pyttsx3
import time
import speech_recognition as sr

openai.api_key = ""

engine = pyttsx3.init()

def translate_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("An Error Occured!")

def generate_response(prompt):
    reponse = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return reponse["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Please Say Ghorbani to Listen your Quesion:")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcript = recognizer.recognize_google(audio)
                if transcript.lower() == "ghorbani":
                    filename = "input.wav"
                    print("Say Your Question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb") as f:
                            f.write(audio.get_wav_data())

                    text = translate_audio_to_text(filename)
                    if text:
                        print("You Said: {text}")

                        response = generate_response(text)
                        print("ChatGPT Said: {response}")

                        speak_text(response)
            except Exception as e:
                print("An Error Occured")

if __name__ == "__main__":
    main
