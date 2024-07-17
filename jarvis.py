import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

load_dotenv()
# Replace this with your Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=gemini_api_key)

# Global variable for WebDriver instance
driver = None

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

# Function to perform a Google search using Selenium
def perform_google_search(query):
    global driver

    try:
        # If driver is not initialized, set it up
        if not driver:
            # Set up Chrome options (without headless mode)
            chrome_options = Options()
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # Initialize the Chrome WebDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open Google
        driver.get("https://www.google.com")

        # Find the search box, enter the query, and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load and get the first result's text
        driver.implicitly_wait(5)
        first_result = driver.find_element(By.CSS_SELECTOR, 'h3').text

        print(f"Search complete. First result: {first_result}")

        return first_result

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to respond based on user query using Gemini
def respond_to_command(query):
    global driver

    if "hello" in query:
        engine.say("Yes, how can I assist you?")
        engine.runAndWait()
        print("Placeholder: Processing query...")
    elif "search for" in query:
        search_query = query.split("search for", 1)[-1].strip()
        result = perform_google_search(search_query)
        if result:
            engine.say(f"The top result is: {result}")
            engine.runAndWait()
            print(f"Top Google search result: {result}")
        else:
            engine.say("Sorry, I couldn't perform the search.")
            engine.runAndWait()
            print("Google search failed.")
    else:
        response = get_genai_response(query)
        engine.say(response)
        engine.runAndWait()
        print(f"Gemini response: {response}")

# Main loop to continuously listen for commands
if __name__ == "__main__":
    try:
        while True:
            command = listen_for_command()
            respond_to_command(command)
    except KeyboardInterrupt:
        # Quit the driver when exiting the program
        if driver:
            driver.quit()
        print("Program terminated.")
