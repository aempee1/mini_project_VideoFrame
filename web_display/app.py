from flask import Flask, render_template, request, flash, redirect, jsonify, url_for, send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set a secret key for the application
bg_video_folder = 'static/bg_video'  # Assuming bg_video is located in the 'static' folder
allowed_extensions = {'mp4', 'avi', 'mov'}  # Set of allowed file extensions

# Set the maximum content length for uploaded files (e.g., 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_latest_uploaded_video(folder_path):
    latest_video = ""
    latest_timestamp = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(('.mp4', '.avi', '.mov')):  # Adjust file extensions as needed
            # Get the timestamp of the file
            timestamp = os.path.getmtime(file_path)
            # Check if the current file is newer than the previous latest file
            if timestamp > latest_timestamp:
                latest_timestamp = timestamp
                latest_video = filename

    return latest_video

@app.route('/')
def index():
    server_ip = request.host.split(':')[0]
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime("%d %B %Y")
    # Assuming you have a function to get the latest uploaded video filename or path
    latest_video = get_latest_uploaded_video("static/bg_video")  # You need to implement this function
    # If you have the filename, you can directly pass it to the template
    return render_template('index.html', current_time=current_time, current_date=current_date, bg_video=latest_video ,server_ip=server_ip)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No file part')
            return redirect(request.url)
        video = request.files['video']
        if video.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if video and allowed_file(video.filename):
            filename = secure_filename(video.filename)  # Secure the filename
            video.save(os.path.join(bg_video_folder, filename))
            # Perform any necessary processing or validation
            return redirect(url_for('upload'))  # Redirect back to the upload page
        else:
            flash('Invalid file type')
            return redirect(request.url)
    return render_template('upload.html')  # Render the upload page template

@app.route('/latest_video')
def latest_video():
    latest_video_name = get_latest_uploaded_video(bg_video_folder)
    return jsonify({'latest_video': latest_video_name})

@app.route('/video/<filename>')
def video(filename):
    return send_from_directory(bg_video_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
