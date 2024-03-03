from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import datetime

# เพิ่มฟังก์ชั่น get_single_image_path
def get_single_image_path(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
        image_files = [file for file in files if file.lower().endswith((".png", ".jpg", ".jpeg"))]

        if len(image_files) == 1:
            return os.path.join(directory, image_files[0])

    return None

def update_time_and_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%B-%Y")
    time_str = now.strftime("%H : %M : %S")

    canvas.delete("text")

    canvas.create_text(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2,
                       text=date_str, font=("Anta", 100, "bold"), fill="white", tag="text", anchor='center', stipple='gray75')
    canvas.create_text(root.winfo_screenwidth() // 2, root.winfo_screenheight() * 0.59,
                       text=time_str, font=("Anta", 70, "bold"), fill="white", tag="text", anchor='center', stipple='gray75')

    root.after(1000, update_time_and_date)

def change_background():
    new_directory = filedialog.askdirectory(title="Select a new image directory")
    new_image_path = get_single_image_path(new_directory)

    if new_image_path:
        # Load and resize the new background image
        new_bg_image = Image.open(new_image_path)
        new_bg_image = new_bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        new_background = ImageTk.PhotoImage(new_bg_image)

        # Clear previous image on canvas
        canvas.delete("background")

        # Display the new background image on the Canvas
        canvas.create_image(0, 0, image=new_background, anchor=NW, tag="background")

        # Update the current image path
        global image_path
        image_path = new_image_path

# Create the Tkinter window
root = Tk()
root.title("Wallpaper Desktop App")

# Specify the directory containing the image file
image_directory = "./uploads/frame1"

# Get the path to the single image in the directory
image_path = get_single_image_path(image_directory)

if image_path:
    # Load and resize the background image
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    background = ImageTk.PhotoImage(bg_image)

    # Create a Canvas as background
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    canvas.pack()

    # Display the background image on the Canvas
    canvas.create_image(0, 0, image=background, anchor=NW, tag="background")

    # Call the recursive function to update Date and Time
    update_time_and_date()

    # Create a button for changing background
    change_bg_button = Button(root, text="Change Background (Space Bar)", command=change_background)
    change_bg_button.pack()

    # Bind the space bar key to the change_background function
    root.bind('<space>', lambda event: change_background())

    # Set the window to full screen
    root.attributes("-fullscreen", True)

    # Run the Tkinter main loop
    root.mainloop()
else:
    print(f"No suitable image file found in the specified directory.")
