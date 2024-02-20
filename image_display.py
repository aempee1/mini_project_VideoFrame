import os
import tkinter as tk
from PIL import Image, ImageTk
import imageio
from datetime import datetime

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
            video_path = os.path.join(self.directory_path, self.media_files[self.file_index])
            self.video = imageio.get_reader(video_path)
            first_frame = self.video.get_data(0)
            self.width, self.height, _ = first_frame.shape
            self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
            self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
            self.canvas.config(width=screen_width, height=screen_height)
            self.update_video()

        # Calculate positions for Canvas and Clock Label
        canvas_x = (screen_width - self.width) // 2
        canvas_y = (screen_height - self.height) // 2
        label_x = self.width // 2
        label_y = self.height // 2

        # Configure canvas to full screen
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.config(width=screen_width, height=screen_height)

        self.clock_label = tk.Label(self.canvas, font=('calibri', 150, 'bold'), background=None, foreground='white')
        self.canvas.create_window(label_x, label_y, window=self.clock_label)

        self.update()

        self.root.attributes("-fullscreen", True)

        self.root.mainloop()

    def update(self):
        if self.is_image:
            # Display image
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        elif self.is_video:
            # Update video frame
            frame = self.video.get_data(0)
            self.photo = self.convert_frame(frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Update clock
        current_time = datetime.now().strftime(' %H : %M ')
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update)  # Update every second
        self.root.after(2, self.check_for_new_media)

    def update_video(self):
        try:
            frame = self.video.get_next_data()
            self.photo = self.convert_frame(frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(10, self.update_video)
        except StopIteration:
            pass

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
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo

# Specify the path of the directory with media files
directory_path = "./uploads/frame1"  # Modify according to the directory you want

app = WallpaperApp(tk.Tk(), directory_path)
