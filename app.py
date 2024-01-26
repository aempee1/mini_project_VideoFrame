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

    # ตรวจสอบว่า Frame Name ตรงกับ directory ที่มีอยู่ใน 'uploads' หรือไม่
    uploads_path = 'uploads'
    existing_frame_names = [folder for folder in os.listdir(uploads_path) if os.path.isdir(os.path.join(uploads_path, folder))]

    if frame_name not in existing_frame_names:
        return 'Invalid Frame Name. Please choose an existing Frame Name.'

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # สร้างโฟลเดอร์สำหรับแต่ละกรอบรูป (ถ้ายังไม่มี)
    if frame_name not in image_paths:
        image_paths[frame_name] = []

    # บันทึกไฟล์ลงใน uploads ด้วยชื่อไฟล์เฉพาะของแต่ละกรอบรูป
    file.save(os.path.join('uploads', frame_name, file.filename))

    # ปรับเปลี่ยน image_paths เป็นไฟล์ใหม่ของแต่ละกรอบรูป
    image_paths[frame_name].append(os.path.join('uploads', frame_name, file.filename))

    return 'File uploaded successfully!'

@app.route('/get_current_images/<frame_name>')
def get_current_images(frame_name):
    return jsonify({'current_image_paths': image_paths.get(frame_name, [])})

if __name__ == '__main__':
    app.run(debug=True)
