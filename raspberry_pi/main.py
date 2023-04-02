from deepface import DeepFace
import json
import cv2
import time
import serial

# Use deepface and cv2 to detect the current emotion of the face on the camera
# and display it on the screen

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Import quotemap.json
f = open("quotemap.json", "r")
quotemap = json.load(f)
f.close()

last_sent = 0

pico = serial.Serial("/dev/ttyACM0", 9600)

def send_emotion(emotion):
    quotes = quotemap[emotion]
    rand_quote = quotes[int(time.time()) % len(quotes)]
    stri = f"%Emotion: {emotion}\n{rand_quote}$"
    pico.write(stri.encode())
    print(stri)

last_emotions = []
last_emotion = "neutral"
while True:
    # Read the frame
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame (stream end)")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect a single face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        try:
            face = img[y:y+h, x:x+w]
            objs = DeepFace.analyze(face, actions = ['emotion'])
            emotions = objs[0]["emotion"]
            # Get the best emotion
            emotion = max(emotions, key=emotions.get)
            last_emotions.append(emotion)
            if len(last_emotions) > 15:
                # Get the most common emotion
                last_emotion = max(set(last_emotions), key=last_emotions.count)
                last_emotions = []

                if time.time() - last_sent > 15:
                    last_sent = time.time()
                    send_emotion(last_emotion)
                    pass
            cv2.putText(img, last_emotion + f"({len(last_emotions)})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Emotion View', img)
        except:
            lat_sent = 0
            last_emotions.clear()
            pass

    # Display

    # Stop if escape key is pressed
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break