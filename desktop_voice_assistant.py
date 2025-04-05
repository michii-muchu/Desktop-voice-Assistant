import pyttsx3 
import speech_recognition as sr
import datetime
import wikipedia 
import webbrowser
import os
import pywhatkit
import pyautogui
import requests
import cv2
from googlesearch import search


engine = pyttsx3.init('sapi5')             
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<16:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am your Desktop assistant Please tell me how may I help you! ")       


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening your voice ~~~~")
        r.pause_threshold = 2
        audio = r.listen(source)
    try:
        print("Trying to Recognize the voice...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Could you please repeat again !")  
        print("Could you please repeat again !")  
        return "None"
    return query

def get_weather(city): 
    api_key = "23c86d8c1aff49cf89b5c2f4d25805f4"
    base_url = f"http://api.openweathermap.org//data//2.5//weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data.get('main',{})
        weather_desc = data['weather'][0].get('description','N/A')
        temp = main.get('temp','N/A')
        humidity = main.get('humidity','N/A')
        weather_report = f"The current temperature in {city} is {temp} degree Celsius with {weather_desc}. The humidity level is at {humidity} percent."
        speak(weather_report) 
        print(weather_report) 
    else: 
        speak("Sorry, I couldn't find the weather for the specified location.")
        print("City Not Found")


def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        key=cv2.waitKey(1) 
        if key==ord('s'): 
            save_directory="C:\\Users\\SHREYA SONI\\OneDrive\\Desktop\\python\\project_desktop_assismtant\\captured images"  
            timestamp=datetime.datetime.now().strftime('%Y%m&d_%H%M%S')
            image_path=os.path.join(save_directory,f'captured_image_{timestamp}.jpg')
            cv2.imwrite(image_path, frame) 
            if os.path.exists(image_path):
                speak('photo is captured!')
                print("Image captured and saved as 'captured_image.jpg'")
        elif key==ord('q'):
            speak('camera closed!')
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
 

        if 'open camera' in query: 
            speak('opening camera') 
            open_camera()


        elif 'wikipedia' in query:
            speak('Searching Wikipedia...') 
            query = query.replace("wikipedia", "").strip() 
            try:
                results = wikipedia.summary(query, sentences=3) 
                speak("According to Wikipedia") 
                speak(results)
                print(results) 
            except wikipedia.exceptions.PageError: 
                speak("Sorry, I could not find any information on that topic.") 
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Multiple results found for {query}. Please be more specific.") 
            except Exception as e:
                speak("An error occurred while searching Wikipedia.") 


        if 'search' in query or 'from google' in query: 
            speak(f'looking for, {query}') 
            query = query.replace("searching", "").strip()
            try:
                url=f"https://www.google.com/search?q={query}" 
                results= search(query, num_results=5)
                webbrowser.open(url) 
                speak(f"Here are the result you are searching for...")
            except Exception as e: 
                speak("An error occurred while searching google.") 
                print(e) 
        

        elif 'weather' in query:
            speak('Please say the name of the city for which you want the weather update.') 
            city = takeCommand()
            get_weather(city)
        
        elif 'open youtube' in query: 
            speak('opening youtube...')
            webbrowser.open("youtube.com")


        elif 'open instagram' in query: 
            speak('opening instagram...')
            webbrowser.open("instagram.com") 


        elif 'open whatsapp' in query: 
            speak('opening whatsapp...') 
            webbrowser.open("whatsapp.com") 


        elif 'open google' in query:
            speak('opening google...') 
            webbrowser.open("google.com") 


        elif 'the time' in query: 
            strTime = datetime.datetime.now().strftime("%I:%M %p") 
            speak(f" The, time is {strTime}")


        elif "today's news" in query:
            speak("Here are the today's top news.....:")
            webbrowser.open("https://news.google.com/home?hl=en-IN&ceid=IN:en&gl=IN") 


        elif 'play music' in query:
            speak("What is the name of the music?") 
            musicName = takeCommand() 
            speak(f'Playing {musicName} on YouTube')
            pywhatkit.playonyt(musicName)
            while True:
                query=takeCommand() 
                if 'stop' in query or 'play' in query:
                    pyautogui.press('k') 
                elif 'mute' in query or 'unmute' in query: 
                    pyautogui.press('m') 
                elif 'full screen the video' in query or 'exit full screen' in query:
                    pyautogui.press('f')
                    break 


        if 'close' in query: 
            print('program closed. see you next time!') 
            speak('program closed. see you next time!') 
            break
               