from flask import Flask, render_template, request, jsonify
import os
import uuid  # เพิ่ม import uuid

app = Flask(__name__ , static_url_path='/static')

# ให้ Flask มีตัวแปร global เพื่อเก็บที่เก็บไฟล์ของแต่ละกรอบรูป
file_paths = {}

@app.route('/')
def index():
    return render_template('index.html', file_paths=file_paths)

@app.route('/upload', methods=['POST'])
def upload():
    global file_paths

    frame_name = request.form['frame_name']

    # ตรวจสอบว่า Frame Name ตรงกับ directory ที่มีอยู่ใน 'uploads' หรือไม่
    uploads_path = 'uploads'
    existing_frame_names = [folder for folder in os.listdir(uploads_path) if os.path.isdir(os.path.join(uploads_path, folder))]

    if frame_name not in existing_frame_names:
        return render_template('Unsucess_page.html')

    if 'file' not in request.files:
        return 'No file part'

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return 'No selected file'

    # สร้างโฟลเดอร์สำหรับแต่ละกรอบรูป (ถ้ายังไม่มี)
    if frame_name not in file_paths:
        file_paths[frame_name] = []
    # ลบไฟล์ทั้งหมดใน directory ของกรอบรูปนั้น ๆ
    # for old_file_path in file_paths[frame_name]:
    #     os.remove(old_file_path)
    # file_paths[frame_name] = []  # เคลียร์รายการไฟล์ทั้งหมดใน file_paths[frame_name]


    # ตรวจสอบว่าไฟล์ที่อัปโหลดเป็นรูปหรือวีดีโอ
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'mkv'}
    file_extension = uploaded_file.filename.rsplit('.', 1)[1].lower() if '.' in uploaded_file.filename else ''

    if file_extension not in allowed_extensions:
        return 'Invalid file format. Please upload an image (jpg, jpeg, png, gif) or a video (mp4, mov, avi, mkv).'

    # สร้างชื่อไฟล์ใหม่โดยใช้ UUID
    new_file_name = str(uuid.uuid4()) + '.' + file_extension
    file_path = os.path.join('uploads', frame_name, new_file_name)

    # บันทึกไฟล์ลงใน uploads ด้วยชื่อไฟล์เฉพาะของแต่ละกรอบรูป
    uploaded_file.save(file_path)

    # ปรับเปลี่ยน file_paths เป็นไฟล์ใหม่ของแต่ละกรอบรูป
    file_paths[frame_name].append(file_path)

    return render_template('Sucess_page.html')

@app.route('/get_current_files/<frame_name>')
def get_current_files(frame_name):
    return jsonify({'current_file_paths': file_paths.get(frame_name, [])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
