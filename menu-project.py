import smtplib
import requests
from bs4 import BeautifulSoup
import pywhatkit as kit
import os
import geocoder
import subprocess
from gtts import gTTS

# Textbelt API key (free-tier key)
textbelt_api_key = 'textbelt'

def send_email():
    try:
        sender = input("Enter sender email: ")
        password = input("Enter password: ")
        recipient = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter message: ")

        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)

        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender, recipient, message)
        print("Email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def text_to_speech():
    try:
        text = input("Enter text to convert to speech: ")
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("open output.mp3")  # For macOS to play the audio file
    except Exception as e:
        print(f"Failed to convert text to speech: {str(e)}")

def get_top5_google_results(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for i, result in enumerate(soup.find_all('h3', limit=5)):
        print(f"{i+1}. {result.text}")

def get_geo_coordinates():
    g = geocoder.ip('me')
    print(f"Your Location: {g.latlng}")

def control_volume(action):
    try:
        if action == 'up':
            subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
        elif action == 'down':
            subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
        else:
            print("Invalid input")
    except Exception as e:
        print(f"Failed to adjust volume: {str(e)}")

def send_sms_textbelt():
    try:
        phone_number = input("Enter recipient's phone number (with country code): ")
        message_body = input("Enter the message to send: ")

        # Send SMS via Textbelt API
        response = requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': message_body,
            'key': textbelt_api_key,
        })

        result = response.json()
        if result['success']:
            print("SMS sent successfully via Textbelt!")
        else:
            print(f"Failed to send SMS: {result['error']}")
    except Exception as e:
        print(f"Error in sending SMS: {str(e)}")

def send_sms_whatsapp():
    try:
        number = input("Enter mobile number (with country code): ")
        message = input("Enter WhatsApp message: ")
        kit.sendwhatmsg_instantly(number, message)
        print("WhatsApp message sent successfully!")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {str(e)}")

def main():
    while True:
        print("\n" + "="*30)
        print("|         Menu Options          |")
        print("="*30)
        print("| 1. Send Email                 |")
        print("| 2. Text-to-Speech             |")
        print("| 3. Get Top 5 Google Results   |")
        print("| 4. Get Current Geo Coordinates|")
        print("| 5. Control Volume             |")
        print("| 6. Send Normal SMS (Textbelt) |")
        print("| 7. Send WhatsApp Message      |")
        print("| 0. Exit                       |")
        print("="*30)
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            send_email()
        elif choice == 2:
            text_to_speech()
        elif choice == 3:
            query = input("Enter search query: ")
            get_top5_google_results(query)
        elif choice == 4:
            get_geo_coordinates()
        elif choice == 5:
            action = input("Increase or Decrease Volume? (up/down): ")
            control_volume(action)
        elif choice == 6:
            send_sms_textbelt()
        elif choice == 7:
            send_sms_whatsapp()
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()