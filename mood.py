import cv2
import numpy as np
from deepface import DeepFace

def getMood(face_cascade, model):
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    cap = cv2.VideoCapture(0)
    success, image = cap.read()
    cv2.imwrite('static/capture.jpg', image)

    faces = face_cascade.detectMultiScale(image, 1.1, 4)

    for (x, y, w, h) in faces:
        face_crop = image[y:y + h, x:x + w]

        # Resize the face image to match the expected input shape of the model
        face_resize = cv2.resize(face_crop, (48, 48))

        # Normalize the pixel values to be between 0 and 1
        face_normal = face_resize / 255.0

        # Reshape the image to match the expected input shape of the model
        face_normal = face_normal.reshape((1, 48, 48, 3))

        # Convert the image data type to float32
        face_normal = face_normal.astype(np.float32)

        # Use model to predict mood
        predictions = model.predict(face_normal)
        emotion_id = np.argmax(predictions)
        emotion = emotions[emotion_id]

    cap.release()
    cv2.destroyAllWindows()

    return emotion