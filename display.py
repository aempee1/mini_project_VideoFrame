import os
import tkinter as tk
from PIL import Image, ImageTk

class ImageGalleryApp:
    def __init__(self, master, image_directory):
        self.master = master
        self.image_directory = image_directory
        self.image_files = self.get_image_files()
        self.current_index = 0

        # ตั้งค่าหน้าจอให้เต็มจอ
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        master.geometry(f"{screen_width}x{screen_height}")

        self.image_label = tk.Label(master)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # แสดงรูปภาพต่อเนื่อง
        self.show_next_image()

    def get_image_files(self):
        # ดึงรายการไฟล์รูปภาพจาก directory
        image_files = [f for f in os.listdir(self.image_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif','.mp4'))]
        image_files.sort()  # เรียงลำดับไฟล์ตามตัวอักษร
        return image_files

    def show_next_image(self):
        if not self.image_files:
            return

        current_image_path = os.path.join(self.image_directory, self.image_files[self.current_index])
        image = Image.open(current_image_path)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        # เลื่อนไปยังรูปถัดไปหลังจาก 3 วินาที
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.master.after(3000, self.check_for_new_images)

    def check_for_new_images(self):
        # ตรวจสอบไฟล์ใหม่ใน directory
        new_image_files = self.get_image_files()

        if new_image_files != self.image_files:
            # หากมีไฟล์ใหม่ให้ลบไฟล์เก่าแล้วปิดหน้าต่าง
            self.remove_old_images()
            self.master.destroy()
            new_root = tk.Tk()
            new_root.title("Automatic Image Gallery App")
            new_root.attributes('-fullscreen', True)  # ตั้งค่า fullscreen
            new_image_gallery_app = ImageGalleryApp(new_root, self.image_directory)
            new_root.mainloop()
        else:
            # หากไม่มีไฟล์ใหม่ให้ตรวจสอบอีกครั้งหลังจาก 3 วินาที
            self.master.after(3000, self.check_for_new_images)

    def remove_old_images(self):
        for old_file in self.image_files:
            file_path = os.path.join(self.image_directory, old_file)
            os.remove(file_path)

def main():
    root = tk.Tk()
    root.title("Automatic Image Gallery App")
    root.attributes('-fullscreen', True)  # ตั้งค่า fullscreen

    image_directory = "./uploads/frame1"  # ระบุ directory ที่เก็บรูปภาพ

    image_gallery_app = ImageGalleryApp(root, image_directory)

    root.mainloop()

if __name__ == "__main__":
    main()
