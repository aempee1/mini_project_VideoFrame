import os
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imageio

class WallpaperApp:
    def __init__(self, root, directory_path):
        self.root = root
        self.root.title("Wallpaper App")

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Set the directory path
        self.directory_path = directory_path

        # List all files in the directory
        self.media_files = self.get_media_files()
        self.file_index = 0

        # Check if the first file is an image or video
        self.is_video = self.media_files and self.media_files[0].lower().endswith(('.mp4', '.avi', '.mov'))
        self.is_image = not self.is_video

        if self.is_image:
            # Load the first image
            img = Image.open(os.path.join(self.directory_path, self.media_files[self.file_index]))
            # Resize image to match screen dimensions
            img = img.resize((screen_width, screen_height))
            self.width, self.height = img.size
            self.photo = ImageTk.PhotoImage(image=img)
        elif self.is_video:
            # Load the first frame of the video
            self.vid = cv2.VideoCapture(os.path.join(self.directory_path, self.media_files[self.file_index]))
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
            self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
            self.canvas.config(width=screen_width, height=screen_height)
            self.update_video()

        # Configure canvas to full screen
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.canvas.config(width=screen_width, height=screen_height)

        self.update()

        self.root.attributes("-fullscreen", True)

        self.root.mainloop()

    def update(self):
        if self.is_image:
            # Display image
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        elif self.is_video:
            # Update video frame
            ret, frame = self.vid.read()
            if ret:
                self.photo = self.convert_frame(frame)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.root.after(10, self.check_for_new_media)

    def update_video(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = self.convert_frame(frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(10, self.update_video)
        else:
            self.vid.release()

    def check_for_new_media(self):
        # Check for new media files in the directory
        new_media_files = self.get_media_files()

        if new_media_files != self.media_files:
            # If there are new files, remove old media and restart the application
            self.remove_old_media()
            self.root.destroy()
            new_root = tk.Tk()
            new_root.title("Wallpaper App")
            new_root.attributes('-fullscreen', True)
            new_wallpaper_app = WallpaperApp(new_root, self.directory_path)
            new_root.mainloop()
        else:
            # If no new files, check again after 3 seconds
            self.root.after(3000, self.check_for_new_media)

    def remove_old_media(self):
        # Remove old media files in the directory
        for old_file in self.media_files:
            file_path = os.path.join(self.directory_path, old_file)
            os.remove(file_path)

    def get_media_files(self):
        # Return a list of media files in the directory
        return [f for f in os.listdir(self.directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov'))]

    def convert_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo

# Specify the path of the directory with media files
directory_path = "./uploads/frame1"  # Modify according to the directory you want

app = WallpaperApp(tk.Tk(), directory_path)
