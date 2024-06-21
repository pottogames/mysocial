from splash import *
from customtkinter import *
from PIL import ImageTk, Image
import webbrowser

def open_ai():
    webbrowser.open("http://127.0.0.1:8000/")

def open_video():
    webbrowser.open("http://127.0.0.1:8000/")

def open_store():
    webbrowser.open('http://127.0.0.1:8000/')

def open_group():
    webbrowser.open('http://127.0.0.1:8000/')

def open_music():
    webbrowser.open('http://127.0.0.1:8000/')

# Create the main application window
app = CTk()
app.title("all in social")
app.geometry("4100x4100")  # Initial size, you can change this if needed
app.attributes('-fullscreen', False)  # Set fullscreen mode
favicon_path = "C:/Users/elia3/Desktop/allinsocial-new1/DesktopApp/icon.ico"
app.iconbitmap(favicon_path)
# Load the main content after the splash screen
image_path = "C:/Users/elia3/Desktop/allinsocial-new1/DesktopApp/logo-transparent.png"
image = Image.open(image_path)
image = ImageTk.PhotoImage(image)
image_label = CTkLabel(master=app, image=image, text="")
image_label.place(relx=0.5, rely=0.2, anchor="center")

frame = CTkFrame(master=app, fg_color="white", border_color="white", corner_radius=32)
frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

# Define common button styles
button_style = {
    "width": 521,
    "height": 72,
    "font": CTkFont(family="Helvetica", size=19, weight="bold"),
    "corner_radius": 32,
    "fg_color": "black",
    "hover_color": "#FF5733",  # Orange hover color
}

btn1 = CTkButton(master=frame, text="Elias AI", command=open_ai, **button_style)
btn1.place(relx=0.5, rely=0.1, anchor="center")

btn2 = CTkButton(master=frame, text="Elias Presentation", command=open_video, **button_style)
btn2.place(relx=0.5, rely=0.3, anchor="center")

btn3 = CTkButton(master=frame, text="Elias Store", command=open_store, **button_style)
btn3.place(relx=0.5, rely=0.5, anchor="center")

btn4 = CTkButton(master=frame, text="Elias Group And Private Channel", command=open_group, **button_style)
btn4.place(relx=0.5, rely=0.7, anchor="center")

btn5 = CTkButton(master=frame, text="Elias Music", command=open_music, **button_style)
btn5.place(relx=0.5, rely=0.9, anchor="center")

# Show the top bar
app.overrideredirect(False)

app.mainloop()