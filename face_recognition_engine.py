import cv2
import os
import numpy as np
import json

class FaceRecognitionEngine:
    def __init__(self, data_dir="data", trainer_dir="trainer", users_file="users.json"):
        self.data_dir = data_dir
        self.trainer_dir = trainer_dir
        self.users_file = users_file
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(trainer_dir, exist_ok=True)

        if os.path.exists(users_file):
            with open(users_file, "r") as f:
                self.users = json.load(f)
        else:
            self.users = {}

        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.model_path = os.path.join(self.trainer_dir, "trainer.yml")

        if os.path.exists(self.model_path):
            self.recognizer.read(self.model_path)

        self.running = False  # recognition flag

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)

    def register_face(self, user_id, user_name, num_samples=50):
        self.users[str(user_id)] = user_name
        self.save_users()

        cam = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                count += 1
                cv2.imwrite(f"{self.data_dir}/User.{user_id}.{count}.jpg", gray[y:y+h,x:x+w])
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.imshow('Registering Face', img)
            if cv2.waitKey(100) & 0xFF == 27:
                break
            elif count >= num_samples:
                break
        cam.release()
        cv2.destroyAllWindows()
        self.train_model()

    def train_model(self):
        faces, ids = [], []
        for file in os.listdir(self.data_dir):
            if file.endswith(".jpg"):
                path = os.path.join(self.data_dir, file)
                gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                id = int(file.split(".")[1])
                faces.append(gray)
                ids.append(id)
        if faces:
            self.recognizer.train(faces, np.array(ids))
            self.recognizer.save(self.model_path)

    def recognize_faces(self):
        self.running = True
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        while self.running:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
                if confidence < 70:
                    name = self.users.get(str(id), f"User {id}")
                    text = f"{name}"
                else:
                    text = "Unknown"
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.putText(img, text, (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.imshow("Face Recognition", img)
            if cv2.waitKey(10) & 0xFF == 27:  # ESC stops recognition
                break

        cam.release()
        cv2.destroyAllWindows()

    def stop_recognition(self):
        self.running = False

    def delete_user(self, user_id):
        files = [f for f in os.listdir(self.data_dir) if f.startswith(f"User.{user_id}.")]
        for f in files:
            os.remove(os.path.join(self.data_dir, f))
        if str(user_id) in self.users:
            del self.users[str(user_id)]
            self.save_users()
        self.train_model()
