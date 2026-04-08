import os
import cv2
import numpy as np

# Шлях до dataset
BASE_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(BASE_DIR, "dataset")

# Беремо готовий xml із OpenCV
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Файл моделі
MODEL_PATH = os.path.join(BASE_DIR, "face_trainer.yml")
LABELS_PATH = os.path.join(BASE_DIR, "labels.txt")
a
# Завантаження каскаду
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

if face_cascade.empty():
    print("❌ Не вдалося завантажити Haar Cascade")
    exit()

# Розпізнавач
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_names = {}
current_label = 0

for person_name in os.listdir(DATASET_PATH):
    person_path = os.path.join(DATASET_PATH, person_name)

    if not os.path.isdir(person_path):
        continue

    label_names[current_label] = person_name

    for file_name in os.listdir(person_path):
        img_path = os.path.join(person_path, file_name)

        image = cv2.imread(img_path)
        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(50, 50)
        )

        for (x, y, w, h) in detected_faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))

            faces.append(face_roi)
            labels.append(current_label)
            break

    current_label += 1

if len(faces) == 0:
    print("❌ Не знайдено жодного обличчя для навчання")
    exit()

recognizer.train(faces, np.array(labels))
recognizer.save(MODEL_PATH)

with open(LABELS_PATH, "w", encoding="utf-8") as f:
    for label, name in label_names.items():
        f.write(f"{label},{name}\n")

print("✅ Навчання завершено успішно")
print("Кількість облич:", len(faces))