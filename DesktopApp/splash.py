from tkinter import Tk, Label
from PIL import Image, ImageTk

# Create the main application window
splash_root = Tk()
splash_root.configure(bg='#F5EBEB')  # Change '#00ff00' to the desired hexadecimal value for the background color
splash_root.overrideredirect(True)  # Remove window decorations
splash_root.attributes('-topmost', True)  # Keep splash screen on top



# Position the main application window in the center of the screen
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
app_x = (screen_width - 700) // 2
app_y = (screen_height - 200) // 2
splash_root.geometry(f'700x200+{app_x}+{app_y}')

# Load the splash screen image
splash_image_path = "C:/Users/elia3/Desktop/allinsocial-new1/DesktopApp/logo-transparent.png"
splash_image = Image.open(splash_image_path)

# Resize the image
target_width = 700  # Set your desired width
target_height = 200  # Set your desired height
splash_image = splash_image.resize((target_width, target_height))

# Convert the resized image to a PhotoImage object
splash_photo = ImageTk.PhotoImage(splash_image)

# Create a Label widget to display the resized image on the splash screen window
splash_label = Label(splash_root, image=splash_photo, bg='#F5EBEB')
splash_label.image = splash_photo  # Store a reference to prevent garbage collection
splash_label.pack()

# Update the window
splash_root.update()

# This is where you would typically perform any initialization tasks
# or load any resources needed for your main application.

# For demonstration purposes, let's simulate a delay
import time
time.sleep(3)

# Close the splash screen window
splash_root.destroy()

# Run the main application event loop
splash_root.mainloop()