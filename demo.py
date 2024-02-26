from tkinter import *
import datetime
from PIL import Image, ImageTk
import os

# recursive function
def update_time_and_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%B-%Y")
    time_str = now.strftime("%H : %M : %S")

    # Clear previous text on canvas
    canvas.delete("text")

    # Display Date and Time on Canvas with transparent background
    canvas.create_text(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2,
                       text=date_str, font=("Anta", 100, "bold"), fill="white", tag="text", anchor='center', stipple='gray75')
    canvas.create_text(root.winfo_screenwidth() // 2, root.winfo_screenheight() * 0.59,
                       text=time_str, font=("Anta", 70, "bold"), fill="white", tag="text", anchor='center', stipple='gray75')

    root.after(1000, update_time_and_date)

def get_single_image_path(directory):
    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Get a list of all files in the directory
        files = os.listdir(directory)

        # Filter for image files (you may need to adjust this based on the types of images you have)
        image_files = [file for file in files if file.lower().endswith((".png", ".jpg", ".jpeg"))]

        # Check if there is exactly one image file
        if len(image_files) == 1:
            # Return the full path to the image file
            return os.path.join(directory, image_files[0])

    # Return None if no suitable image file is found
    return None

root = Tk()
root.title("Wallpaper Desktop App")

# Specify the directory containing the image file
image_directory = "./uploads/frame1"

# Get the path to the single image in the directory
image_path = get_single_image_path(image_directory)

# Check if the image file exists
if image_path:
    # Load and resize the background image
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    background = ImageTk.PhotoImage(bg_image)

    # Create a Canvas as background
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    canvas.pack()

    # Display the background image on the Canvas
    canvas.create_image(0, 0, image=background, anchor=NW)

    # Call the recursive function to update Date and Time
    update_time_and_date()

    # Set the window to full screen
    root.attributes("-fullscreen", True)

    root.mainloop()
else:
    print(f"No suitable image file found in the specified directory.")
