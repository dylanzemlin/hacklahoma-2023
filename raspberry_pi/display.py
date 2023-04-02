import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk

class Display:
    def __init__(self, window, cap):
        self.window = window
        self.cap = cap
        self.window.title("Droid GUI")
        self.window.geometry("1920x1080")

        self.panedwindow = tk.PanedWindow(window, orient=tk.HORIZONTAL)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        self.left_pane = tk.Frame(self.panedwindow)
        self.panedwindow.add(self.left_pane)

        self.right_pane = tk.Frame(self.panedwindow)
        self.panedwindow.add(self.right_pane)

        self.canvas = tk.Canvas(self.left_pane, width=800, height=600)
        self.canvas.pack()

        self.label = tk.Label(self.right_pane, text="This GUI is garbage \n but its alright")
        self.label.pack()

        self.delay = 15
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = PIL.Image.fromarray(frame)
            image = image.resize((800, 600))
            photo = PIL.ImageTk.PhotoImage(image)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.photo = photo

        self.window.after(self.delay, self.update)

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    window = tk.Tk()

    app = Display(window, cap)

    window.mainloop()

    cap.release()
