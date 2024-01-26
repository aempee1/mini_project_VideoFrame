from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# ให้ Flask มีตัวแปร global เพื่อเก็บที่เก็บรูปภาพของแต่ละกรอบรูป
image_paths = {}

@app.route('/')
def index():
    return render_template('index.html', image_paths=image_paths)

@app.route('/upload', methods=['POST'])
def upload():
    global image_paths

    frame_name = request.form['frame_name']

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # ตรวจสอบว่าโฟลเดอร์สำหรับ Frame Name นี้มีอยู่หรือไม่
    frame_folder = os.path.join('uploads', frame_name)
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    # บันทึกไฟล์ลงในโฟลเดอร์นี้
    file.save(os.path.join(frame_folder, file.filename))

    # ปรับเปลี่ยน image_paths เป็นไฟล์ใหม่ของแต่ละกรอบรูป
    if frame_name not in image_paths:
        image_paths[frame_name] = []

    image_paths[frame_name].append(os.path.join(frame_folder, file.filename))

    return 'File uploaded successfully!'

@app.route('/get_current_images/<frame_name>')
def get_current_images(frame_name):
    return jsonify({'current_image_paths': image_paths.get(frame_name, [])})

if __name__ == '__main__':
    app.run(debug=True)
