import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import serial
import threading
from deepface import DeepFace

class Display:
    def __init__(self, window, cap):
        self.window = window
        self.cap = cap
        self.window.title("Galatic Mood Monitor")
        self.window.geometry("1920x1080")

        self.panedwindow = tk.PanedWindow(window, orient=tk.HORIZONTAL)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        self.left_pane = tk.Frame(self.panedwindow)
        self.panedwindow.add(self.left_pane)

        self.right_pane = tk.Frame(self.panedwindow)
        self.panedwindow.add(self.right_pane)

        self.canvas = tk.Canvas(self.left_pane, width=800, height=600)
        self.canvas.pack()

        self.label = tk.Label(self.right_pane, text="Last Emotion: ")
        self.label.pack()

        self.age_label = tk.Label(self.right_pane, text="Age: ")
        self.age_label.pack()

        # Print Receipt Button
        self.button = tk.Button(self.right_pane, text="Print Receipt", command=self.print_receipt)
        self.button.pack()

        self.emotions = []

        self.delay = 1
        self.last_frame = None
        self.last_coords = None
        self.end = False
        self.emotion_thread = threading.Thread(target=self.emotion_analysis)
        self.emotion_thread.daemon = True
        self.emotion_thread.start()
        self.pico = serial.Serial('/dev/ttyACM0', 9600)
        self.update()

    def print_receipt(self):
        self.pico.write("%$".encode())
        emotion = self.label.cget("text").split(": ")[1]
        self.pico.write(f"{emotion.strip()}".encode())
        self.pico.write("this is an epic quote$".encode())

    def emotion_analysis(self):
        if self.end:
            return
        
        if self.last_frame is None or self.last_coords is None:
            time.sleep(0.5)
            self.emotion_analysis()
            return

        try:
            frame = self.last_frame
            x, y, w, h = self.last_coords
            try:
                face = frame[y:y+h, x:x+w]
                objs = DeepFace.analyze(face, actions = ['emotion'])
                emotions = objs[0]["emotion"]
                emotion = max(emotions, key=emotions.get)
                self.emotions.append(emotion)
                if len(self.emotions) > 8:
                    # Pop the first element
                    self.emotions.pop(0)

                # Get the most common emotion
                emotion = max(set(self.emotions), key=self.emotions.count)
                self.label.config(text=f"Last Emotion: {emotion}")

                time.sleep(0.5)
                self.emotion_analysis()
            except:
                time.sleep(0.5)
                self.emotion_analysis()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.end = True
            exit()

    def update(self):
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w,y + h), (0, 255, 0), 2)

                    # Display image :)
                    image = PIL.Image.fromarray(frame)
                    image_resized = image.resize((800, 600))
                    photo = PIL.ImageTk.PhotoImage(image_resized)
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                    self.canvas.photo = photo

                    self.last_coords = (x, y, w, h)
                    self.last_frame = frame

                    break

            self.window.after(50, self.update)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            self.end = True
            exit()

if __name__ == "__main__":
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        window = tk.Tk()
        app = Display(window, cap)
        window.mainloop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        exit()