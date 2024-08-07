import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Image Capture")
        self.root.geometry("800x600")

        self.label_var = tk.StringVar()
        self.label_var.set("Press 'Start' to begin capturing images.")

        self.language_var = tk.StringVar(value="SIBI")
        self.language_var.trace_add('write', self.update_labels)

        self.language_label = tk.Label(self.root, text="Select Language:")
        self.language_label.pack(pady=10)

        self.language_dropdown = tk.OptionMenu(self.root, self.language_var, "SIBI", "BISINDO")
        self.language_dropdown.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_capture)
        self.start_button.pack(pady=20)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_capture, state=tk.DISABLED)
        self.pause_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_capture, state=tk.DISABLED)
        self.quit_button.pack(pady=10)

        self.status_label = tk.Label(self.root, textvariable=self.label_var, font=('Helvetica', 14))
        self.status_label.pack(pady=20)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)

        self.root.bind('<space>', self.toggle_pause)

        self.cap = None
        self.paused = False
        self.count = 0
        self.current_label = None
        self.num_images_per_label = 100
        self.labels = {
            "SIBI": [str(i) for i in range(10)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)],
            "BISINDO": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        }
        self.save_dir = 'dataset'
        self.update_labels()

    def update_labels(self, *args):
        current_language = self.language_var.get()
        self.labels_to_capture = self.labels[current_language]

    def start_capture(self):
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.quit_button.config(state=tk.NORMAL)
        self.capture_images()

    def pause_capture(self):
        self.paused = not self.paused
        self.update_pause_button()

    def toggle_pause(self, event):
        self.pause_capture()

    def update_pause_button(self):
        if self.paused:
            self.pause_button.config(text="Resume")
            self.label_var.set("Capture paused. Press 'Resume' to continue or press 'Space' to resume.")
        else:
            self.pause_button.config(text="Pause")
            self.label_var.set("Capture resumed. Press 'Pause' to pause again or press 'Space' to pause.")

    def quit_capture(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
        self.root.destroy()

    def capture_images(self):
        current_language = self.language_var.get()
        for label in self.labels_to_capture:
            self.current_label = label
            self.count = 0
            
            self.label_var.set(f"Get ready to capture images for label: {label}. Press 'Space' to start capturing.")
            self.root.update()

            # Wait for user to press space to start capturing
            while not self.paused:
                self.root.wait_variable(self.label_var)  # Wait for an event
                if self.paused:
                    break
            
            save_path = os.path.join(self.save_dir, current_language)
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            self.cap = cv2.VideoCapture(0)
            self.paused = False  # Start capturing images

            while self.count < self.num_images_per_label:
                ret, frame = self.cap.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.image_label.imgtk = imgtk
                self.image_label.configure(image=imgtk)

                if not self.paused:
                    image_path = os.path.join(save_path, f'{label}_{self.count}.jpg')
                    cv2.imwrite(image_path, frame)
                    self.count += 1
                    self.label_var.set(f'Captured {self.count}/{self.num_images_per_label} for label: {label}')
                    self.root.update()

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.quit_capture()
                    return

            self.cap.release()
            self.label_var.set(f'Finished capturing images for label: {label}')
            self.root.update()
        
        self.label_var.set("All labels captured. Press 'Quit' to exit.")
        self.pause_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.NORMAL)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCaptureApp(root)
    root.mainloop()
