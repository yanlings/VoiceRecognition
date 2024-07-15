import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
        return response.lower()
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"

def search_google(query):
    driver = webdriver.Chrome()
    driver.get('http://www.google.com')
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Let the user actually see something!
    driver.quit()

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for 'Hey Jarvis'...")

    while True:
        print("Say 'Hey Jarvis' to start...")
        command = recognize_speech_from_mic(recognizer, microphone)
        if "hey jarvis" in command:
            print("I'm listening...")
            search_query = recognize_speech_from_mic(recognizer, microphone)
            print(f"Searching for: {search_query}")
            search_google(search_query)

if __name__ == "__main__":
    main()
