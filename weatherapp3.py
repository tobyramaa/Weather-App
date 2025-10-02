from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import requests
import pyttsx3 # Text-to-Speech
from PIL import Image, ImageTk

# OUR API key
API_KEY = "f85211d4459bfd41ebd1b367692bb0d2"

#Prediction Function
def predict_weather(temp, humidity, condition):
    if "rain" in condition.lower() or humidity > 80:
        prediction = "Possible rain(High Humidity)"
        advice = "Take your umbrella, it might rain."
    elif "thunder" in condition.lower():
        prediction = "Thunderstorm"
        advice = "Stay indoors, thunderstorm expected."
    elif "snow" in condition.lower() or temp <= 2:
        prediction = "Snowy"
        advice = "Dress warmly, snow is expected."
    elif temp >= 30:
        prediction = "Sunny / Hot"
        advice = "Wear light clothes and stay hydrated."
    elif 20 <= temp < 30:
        prediction = "Warm"
        advice = "Nice weather, enjoy your day."
    elif 10 <= temp < 20:
        prediction = "Cool"
        advice = "A jacket would be useful."
    elif 3 <= temp < 10:
        prediction = "Cold"
        advice = "Dress warmly, it's cold outside."
    else:
        prediction = "uncertain!"
        advice = "Enjoy your day!"
    return prediction, advice


 
my_win = Tk()
my_win.title("Weather App")
window_width = 900
window_height = 500


screen_width = my_win.winfo_screenwidth()
screen_height = my_win.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

my_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
my_win.resizable(False, False)


#  Fetch Weather Function 
def get_weather():
    city = textfield.get()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name")
        return

    try:
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        weather = response.json()

        if weather.get("cod") != 200:
            messagebox.showerror(
                "Error",
                f"Weather data not found for '{city}'\nReason: {weather.get('message', 'Unknown error')}"
            )
            return

        
        timezone_offset = weather["timezone"]  
        utc_time = datetime.utcnow()
        local_time = utc_time + timedelta(seconds=timezone_offset)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT TIME")

        # Extract weather data
        condition = weather["weather"][0]["main"]   
        description = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]
        pressure = weather["main"]["pressure"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]

        # Update labels
        t.config(text=f"{temp}°C")
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")
        w.config(text=f"{wind} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=description)
        p.config(text=f"{pressure} hPa")

        # Prediction + Advice
        prediction, advice = predict_weather(temp, humidity, condition)
        pred_label.config(text=f"Prediction: {prediction}")
        advice_label.config(text=f"Advice: {advice}")

        #Icon  
        icon_path = "images/logo.png"  
        text_color = "black"

        if "rain" in condition.lower():
            icon_path = "images/rain.png"
            text_color = "blue"
        elif "cloud" in condition.lower():
            icon_path = "images/cloud.png"
            text_color = "gray"
        elif "clear" in condition.lower():
            icon_path = "images/sun.png"
            text_color = "orange"
        elif "snow" in condition.lower():
            icon_path = "images/snow.png"
            text_color = "lightblue"
        elif "thunder" in condition.lower():
            icon_path = "images/storm.png"
            text_color = "red"

        # Resize icon to match logo size
        img = Image.open(icon_path).convert("RGBA")
        img = img.resize((logo_width, logo_height), Image.LANCZOS)
        new_icon = ImageTk.PhotoImage(img)

        # Update logo
        logo.config(image=new_icon)
        logo.image = new_icon 

      
        pred_label.config(fg=text_color)
        advice_label.config(fg=text_color)

        #  Refresh GUI so changes appear before voice
        my_win.update()

        # 🔊 Text-to-Speech
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Change to voices[1] for female

        speech = f"The weather in {city} is {description}. Temperature is {temp} degrees Celsius. " \
                 f"Humidity is {humidity} percent. Wind speed is {wind} meters per second. " \
                 f"The time is {current_time} in {city}. Prediction: It looks {prediction}. {advice}"
        engine.say(speech)
        engine.runAndWait()

    except Exception as e:
        messagebox.showerror("Weather App", f"Invalid Entry or Network Issue\n\n{e}")


#GUI 
search_image = PhotoImage(file="images/search.png")
myimage = Label(image=search_image)
myimage.place(x=20, y=20)

textfield = Entry(my_win, justify="center", width=17, font=("poppins", 25, "bold"),
                  bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="images/search_icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2",
                      bg="#404040", command=get_weather)
myimage_icon.place(x=400, y=34)


default_img = Image.open("images/logo.png").convert("RGBA")
default_logo = ImageTk.PhotoImage(default_img)
logo = Label(image=default_logo)
logo.place(x=150, y=100)


logo_width, logo_height = default_img.size

Frame_image = PhotoImage(file="images/box.png")
Frame_myimage = Label(image=Frame_image)
Frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

name = Label(my_win, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(my_win, font=("Helvetica", 20))
clock.place(x=30, y=130)

label1 = Label(my_win, text="WIND", font=("Helvetica", 15, "bold"),
               fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(my_win, text="HUMIDITY", font=("Helvetica", 15, "bold"),
               fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(my_win, text="DESCRIPTION", font=("Helvetica", 15, "bold"),
               fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(my_win, text="PRESSURE", font=("Helvetica", 15, "bold"),
               fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)


pred_label = Label(my_win, font=("arial", 15, "bold"), fg="blue")
pred_label.place(x=400, y=300)

advice_label = Label(my_win, font=("arial", 12, "bold"), fg="green")
advice_label.place(x=400, y=330)

my_win.mainloop()

