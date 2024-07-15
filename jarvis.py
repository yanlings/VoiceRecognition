import speech_recognition as sr
import pyttsx3
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

load_dotenv()
# Replace this with your Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=gemini_api_key)

# Function to listen for wake word and process query
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, speech service is down.")
        return ""

# Function to interact with Gemini and get a response
# Function to interact with GenAI and get a response
def get_genai_response(command):
    if command:
        response = model.generate_content(command)

        if response and response.candidates:
            # Assuming you want the first candidate's text content
            content_parts = response.candidates[0].content.parts
            response_text = "".join(part.text for part in content_parts)
            return response_text.strip()
        else:
            print("Error: Empty or invalid response from GenAI.")
            return "Sorry, I couldn't process that."
    else:
        print("Error: Empty command received.")
        return "Sorry, I couldn't process that."



# Function to respond based on user query using Gemini
def respond_to_command(query):
    if "hello" in query:
        engine.say("Yes, how can I assist you?")
        engine.runAndWait()
        print("Placeholder: Processing query...")
    else:
        response = get_genai_response(query)
        engine.say(response)
        engine.runAndWait()
        print(f"Gemini response: {response}")

# Main loop to continuously listen for commands
if __name__ == "__main__":
    while True:
        command = listen_for_command()
        respond_to_command(command)
