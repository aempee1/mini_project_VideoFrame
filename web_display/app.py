from flask import Flask, render_template
from datetime import datetime
import os
import shutil
import time

app = Flask(__name__)
bg_image_folder = "static/bg_image"  # Assuming bg_image is located in the 'static' folder

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime("%d %B %Y")

    # Check for new files in the bg_image folder
    new_files = get_new_files()
    if new_files:
        # Delete old files and replace with new files
        delete_old_files(new_files)
        replace_files(new_files)

        # Restart the server after replacing files
        restart_server()

    return render_template('index.html', current_time=current_time, current_date=current_date)

def get_new_files():
    # Get the list of current files in the bg_image folder
    current_files = os.listdir(bg_image_folder)

    # Sort files by modification time in descending order
    current_files.sort(key=lambda x: os.path.getmtime(os.path.join(bg_image_folder, x)), reverse=True)

    # Check if there are at least 2 files (current and previous)
    if len(current_files) > 1:
        return [current_files[0]]  # Return only the newest file
    else:
        return []

def delete_old_files(new_files):
    # Delete old files in the bg_image folder, except for the newest file
    for filename in os.listdir(bg_image_folder):
        if filename not in new_files:
            file_path = os.path.join(bg_image_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {filename}: {e}")

def replace_files(new_files):
    # Replace old files with new files
    for new_file in new_files:
        new_file_path = os.path.join(bg_image_folder, new_file)
        old_file_path = os.path.join(bg_image_folder, "video1.mp4")  # Replace with the old file's name
        try:
            shutil.copy(new_file_path, old_file_path)
        except Exception as e:
            print(f"Error replacing file {new_file}: {e}")

def restart_server():
    print("Restarting the server...")
    time.sleep(2)  # Give some time for the response to be sent
    os._exit(0)  # Terminate the current Python process

if __name__ == '__main__':
    app.run(debug=True)
