from deepface import DeepFace
import cv2

# Use deepface and cv2 to detect the current emotion of the face on the camera
# and display it on the screen

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

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
            if len(last_emotions) > 5:
                # Get the most common emotion
                last_emotion = max(set(last_emotions), key=last_emotions.count)
                last_emotions = []
            cv2.putText(img, last_emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Emotion View', img)
        except:
            pass

    # Display

    # Stop if escape key is pressed
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break