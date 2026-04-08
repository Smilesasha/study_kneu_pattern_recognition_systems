import cv2
import os
import matplotlib.pyplot as plt

# -------------------------------------------------
# Шляхи до каскадів OpenCV
# -------------------------------------------------
FACE_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
EYE_CASCADE = cv2.data.haarcascades + "haarcascade_eye.xml"
SMILE_CASCADE = cv2.data.haarcascades + "haarcascade_smile.xml"

# -------------------------------------------------
# Завантаження каскадів
# -------------------------------------------------
face_cascade = cv2.CascadeClassifier(FACE_CASCADE)
eye_cascade = cv2.CascadeClassifier(EYE_CASCADE)
smile_cascade = cv2.CascadeClassifier(SMILE_CASCADE)

if face_cascade.empty() or eye_cascade.empty() or smile_cascade.empty():
    print("❌ Не вдалося завантажити один або кілька cascade-файлів.")
    exit()

# -------------------------------------------------
# Шлях до зображення
# -------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(BASE_DIR, "test.jpg")

# -------------------------------------------------
# Завантаження зображення
# -------------------------------------------------
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("❌ Не вдалося завантажити test.jpg")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# -------------------------------------------------
# Пошук облич
# -------------------------------------------------
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(80, 80)
)

if len(faces) == 0:
    print("Обличчя не знайдено")
else:
    print(f"Знайдено облич: {len(faces)}")

# -------------------------------------------------
# Аналіз кожного обличчя
# -------------------------------------------------
for (x, y, w, h) in faces:
    face_roi_gray = gray[y:y+h, x:x+w]
    face_roi_color = image[y:y+h, x:x+w]

    # Пошук очей
    eyes = eye_cascade.detectMultiScale(
        face_roi_gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(20, 20)
    )

    # Пошук усмішки
    smiles = smile_cascade.detectMultiScale(
        face_roi_gray,
        scaleFactor=1.7,
        minNeighbors=20,
        minSize=(25, 25)
    )

    # Евристичне визначення емоції
    if len(smiles) > 0:
        emotion = "happy"
        color = (0, 255, 0)
    elif len(eyes) >= 2:
        emotion = "neutral"
        color = (255, 0, 0)
    else:
        emotion = "serious"
        color = (0, 0, 255)

    # Малюємо рамку обличчя
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

    # Підпис
    cv2.putText(
        image,
        emotion,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )

    # Малюємо очі
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(face_roi_color, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 1)

    # Малюємо усмішку
    for (sx, sy, sw, sh) in smiles:
        cv2.rectangle(face_roi_color, (sx, sy), (sx + sw, sy + sh), (0, 255, 255), 1)

# -------------------------------------------------
# Показ результату через matplotlib
# -------------------------------------------------
plt.figure(figsize=(8, 8))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Emotion recognition with OpenCV")
plt.axis("off")
plt.show()