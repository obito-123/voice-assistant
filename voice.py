import os
import random
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia
import smtplib
import requests
import json
from urllib.request import urlopen

# Clear screen FIRST (before other imports that might error)
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 190)

# Global variables
assname = "Jarvis"

def speak(audio):
    """Convert text to speech"""
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greet user based on time"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"I am {assname}, Sir. Please tell me how may I help you")

def takeCommand():
    """VOICE ONLY - loops until speech detected"""
    r = sr.Recognizer()
    while True:  # Loop until voice detected
        try:
            print("🔴 Listening... Speak now!")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            print("🧠 Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"👤 You said: {query}\n")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("⏳ No speech - listening again...")
            continue
            
        except sr.UnknownValueError:
            print("❓ Could not understand - speak clearly...")
            continue
            
        except sr.RequestError as e:
            print("🌐 Google API error - check internet...")
            speak("Internet error, using text input")
            return input("Type command: ").lower()

def sendEmail(to, content):
    """Send email (configure your credentials)"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your-email@gmail.com", "your-app-password")  # Use App Password
        server.sendmail("your-email@gmail.com", to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        speak("Sorry, I couldn't send the email")

if __name__ == "__main__":
    wishMe()
    
    while True:
        query = takeCommand()
        
        # Wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        # Open websites
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("Here you go to Youtube")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("Here you go to Google")
            
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            speak("Here you go to Stack Overflow. Happy coding")
            
        # Play music
        elif 'play music' in query or 'play song' in query:
            music_dir = os.path.join(os.path.expanduser("~"), "Music")
            try:
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    speak("Playing music")
                else:
                    speak("No music found in Music folder")
            except:
                speak("Music folder not accessible")
                
        # Time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            
        # Email
        elif 'email to gaurav' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "gaurav@example.com"
                sendEmail(to, content)
            except Exception as e:
                speak("Sorry, I couldn't send the email")
                
        # Name functions
        elif "what's your name" in query or "what is your name" in query:
            speak(f"My friends call me {assname}")
            
        elif "change name" in query:
            speak("What would you like to call me?")
            new_name = takeCommand().replace("call me ", "")
            assname = new_name
            speak(f"Thanks for naming me {assname}")
            
        # Exit
        elif 'exit' in query or 'bye' in query:
            speak("Thanks for giving me your time")
            exit()
            
        # Creator
        elif 'who made you' in query or 'who created you' in query:
            speak("I have been created by Shreyas Ballari")

        elif 'who i am' in query:
            speak("you are bsdk")   
            
        # Search
        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open(f"https://google.com/search?q={query}")
            speak("Searching Google")
            
        # Location
        elif "open map" in query:
            query = query.replace("where is", "")
            webbrowser.open(f"https://google.nl/maps/place/{query}")
            speak("Showing location")

        elif 'start attendance' in query or 'face attendance' in query:
            speak("Activating face recognition attendance system!")
            speak("Look at the camera Sir!")
            # [Your face recognition code here]
            import cv2
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Jarvis Attendance', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            speak("Attendance session completed!")
            
        elif 'open camera' in query:
            speak("Opening camera for you!")
            import cv2
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Jarvis Camera', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            speak("Camera closed!")
        
    # EVERY COMMAND NEEDS speak()!
        elif 'how are you' in query:
            speak("I am doing excellent Sir, thank you for asking!")
            speak("How are you today?")
            
        elif 'joke' in query:
            speak("Here's a great joke for you Sir!")
            jokes = ["Why don't scientists trust atoms? They make up everything!",
                    "Parallel lines have so much in common. It's a shame they'll never meet!"]
            joke = random.choice(jokes)
            speak(joke)
            speak("Was that funny Sir?")
            
        elif 'weather' in query:
            speak("Let me check the weather for you!")
            speak("What city would you like weather for?")
            city = takeCommand()
            speak(f"Opening weather for {city}!")
            webbrowser.open(f"https://google.com/search?q=weather+{city}")
            
        elif 'news' in query:
            speak("Fetching latest news headlines!")
            webbrowser.open("https://news.google.com")
            speak("News ready Sir!")
            
        elif 'exit' in query or 'bye' in query:
            speak("Thank you for your time Sir!")
            speak(f"Goodbye from {assname}!")
            exit()
            
       
    # Default responses
        elif "who i am" in query:
            speak("you are a shreyas ballari and you are kind person ")
                
        elif 'how are you' in query:
            speak("I am fine, thank you. How are you, Sir?")
                
        else:
            speak("Sorry, I didn't understand that. Try: open youtube, the time, or exit")

            
