import os
import cv2

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "face_trainer.yml")
LABELS_PATH = os.path.join(BASE_DIR, "labels.txt")

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    print("❌ Не вдалося завантажити Haar Cascade")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

label_names = {}
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        label, name = line.strip().split(",")
        label_names[int(label)] = name

image_path = os.path.join(BASE_DIR, "test.jpg")
image = cv2.imread(image_path)

if image is None:
    print("❌ Не вдалося завантажити test.jpg")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(50, 50)
)

for (x, y, w, h) in faces:
    face_roi = gray[y:y+h, x:x+w]
    face_roi = cv2.resize(face_roi, (200, 200))

    label, confidence = recognizer.predict(face_roi)

    if confidence < 80:
        name = label_names.get(label, "Unknown")
    else:
        name = "Unknown"

    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(
        image,
        f"{name} ({confidence:.1f})",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

cv2.imshow("Face Recognition", image)
cv2.waitKey(0)
cv2.destroyAllWindows()