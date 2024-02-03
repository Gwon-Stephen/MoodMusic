import cv2
import numpy as np
from deepface import DeepFace

def getMood(face_cascade, model):
    emotions = ['angry', 'angry', 'sad', 'happy', 'sad', 'happy', 'neutral']
    emotion = 'happy'

    cap = cv2.VideoCapture(0)
    success, image = cap.read()
    cv2.imwrite('static/capture.jpg', image)

    height, width, channels = image.shape
    screen_center_x = width / 2
    screen_center_y = height / 2

    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minSize=(40, 40))

    if len(faces) > 0:
        main_face_distance = float('inf')
        main_face_x, main_face_y, main_face_w, main_face_h = 0, 0, 0, 0

        for (x, y, w, h) in faces:
            face_center_x = x + (w / 2)
            face_center_y = y + (h / 2)

            curr_face_distance = ((face_center_x - screen_center_x)**2 + (face_center_y - screen_center_y)**2)**0.5

            if main_face_distance > curr_face_distance:
                main_face_x, main_face_y, main_face_w, main_face_h = x, y, w, h
                main_face_distance = curr_face_distance

        face_crop = image[main_face_y:main_face_y + main_face_h, main_face_x:main_face_x + main_face_w]
        face_resize = cv2.resize(face_crop, (48, 48))
        face_normal = face_resize / 255.0
        face_normal = face_normal.reshape((1, 48, 48, 3))
        face_normal = face_normal.astype(np.float32)
        
        predictions = model.predict(face_normal)
        emotion_id = np.argmax(predictions)
        emotion = emotions[emotion_id]
        cv2.rectangle(image, (main_face_x, main_face_y), (main_face_x + main_face_w, main_face_y + main_face_h), (0, 0, 255), 2)
        cv2.putText(image, emotion, (main_face_x, main_face_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


    cap.release()
    return emotion