from deepface import DeepFace
import cv2

# Use deepface and cv2 to detect the current emotion of the face on the camera
# and display it on the screen

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
print("Getting video capture from webcam")
cap = cv2.VideoCapture(0)
print("Video capture from webcam is ready")
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

while True:
    # Read the frame
    print("Reading frame from video capture")
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
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
            emotion = max(emotions.items(), key=lambda x: x[1])
            cv2.putText(img, emotion[0], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Emotion View', img)
        except:
            pass

    # Display

    # Stop if escape key is pressed
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break