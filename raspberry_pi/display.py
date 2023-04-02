import tkinter as tk
import cv2
import requests
import PIL.Image, PIL.ImageTk
import time
import serial
import threading
from deepface import DeepFace

f = open(".env", "r")
lines = f.readlines()
f.close()

# Load Environment Variables
env = {}
for line in lines:
    line = line.strip()
    if line.startswith("#"):
        continue
    key, value = line.split("=")
    env[key.strip()] = value.strip()

def prompt(text, model):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + env["OPENAI_TOKEN"],
        "OpenAI-Organization": env["OPENAI_ORG_ID"]
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data, timeout=3)
    json = response.json()
    if json["object"] != "chat.completion":
        return "Error"
    return json["choices"][0]["message"]["content"]

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
        self.last_emotion = None
        self.pico = serial.Serial('/dev/ttyACM0', 9600)
        self.update()

    def print_receipt(self):
        if self.last_emotion is None:
            return

        try:
            quote = prompt(f"Generate a inspiration quote, my current emotional state is {self.last_emotion.strip()}. Make it starwars themed", "gpt-3.5-turbo")
            self.pico.write("%$".encode())
            self.pico.write(f"{self.last_emotion.strip()}$".encode())
            self.pico.write(f"{quote}$".encode())
        except:
            self.pico.write("%$".encode())
            self.pico.write(f"{self.last_emotion.strip()}$".encode())
            self.pico.write("Error fetching quote$".encode())

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
                self.last_emotion = emotion
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
                    cv2.putText(frame, self.last_emotion + f"({len(self.last_emotion)})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

                    # Display image :)
                    image = PIL.Image.fromarray(frame)
                    image_resized = image.resize((800, 600))
                    photo = PIL.ImageTk.PhotoImage(image_resized)
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                    self.canvas.photo = photo

                    self.last_coords = (x, y, w, h)
                    self.last_frame = frame

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