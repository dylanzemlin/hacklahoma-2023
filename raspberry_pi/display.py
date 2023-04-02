import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
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
        self.update()

    def print_receipt(self):
        pass

    def update(self):
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0, 255, 0),2)

                image = PIL.Image.fromarray(frame)
                image_resized = image.resize((800, 600))
                photo = PIL.ImageTk.PhotoImage(image_resized)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.canvas.photo = photo

                try:
                    face = frame[y:y+h, x:x+w]
                    objs = DeepFace.analyze(face, actions = ['emotion'])
                    emotions = objs[0]["emotion"]
                    # age = objs[0]["age"]
                    # self.age_label.config(text=f"Age: {age}")
                    # Get the best emotion
                    emotion = max(emotions, key=emotions.get)
                    self.emotions.append(emotion)
                    if len(self.emotions) > 15:
                        # Pop the first element
                        self.emotions.pop(0)

                    # Get the most common emotion
                    emotion = max(set(self.emotions), key=self.emotions.count)
                    self.label.config(text=f"Last Emotion: {emotion}")
                except:
                    self.window.after(50, self.update)
                    pass

            self.window.after(50, self.update)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
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