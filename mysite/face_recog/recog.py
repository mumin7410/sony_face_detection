import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from .models import Transaction
from django.core.files import File
import os
import tempfile
from pathlib import Path
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from django.utils import timezone
import threading

class FaceRecognition:
    def __init__(self):
        self.stay_still_arr = []
        self.stay_still_lock = threading.Lock()  # Lock for synchronization
        self.thread_pool = ThreadPoolExecutor(max_workers=4)

    def face_compare(self, result, temp_face_path):
        if len(result[0]) == 0:
            name = 'Stranger !!!'
            # post data
            transaction = Transaction(EmployeeID=0,Name=name,DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),CameraNo=1,Image=File(open(Path(temp_face_path).relative_to(settings.BASE_DIR), "rb")))
            transaction.save()
        else:
            s = result[0]['identity'][0]
            x = s.split('/')[6]
            EmployeeID = x.split('_')[0] #EmpID
            Name = x.split('_')[1]

            EmployeeID = EmployeeID.replace(':', '')
            Name = Name.replace(':', '')

            # Acquire lock before accessing stay_still_arr
            with self.stay_still_lock:
                employee_in_arr = False
                for item in self.stay_still_arr:
                    if item['EmployeeID'] == EmployeeID:
                        employee_in_arr = True
                        time_difference = timezone.now() - datetime.strptime(item['DateTime'], '%Y-%m-%d %H:%M:%S')
                        if time_difference.total_seconds() > 300:
                            # post data
                            transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'), CameraNo=1, Image=File(open(Path(temp_face_path).relative_to(settings.BASE_DIR), "rb")))
                            transaction.save()
                            self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
                if not employee_in_arr:
                    # post data
                    transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'), CameraNo=1, Image=File(open(Path(temp_face_path).relative_to(settings.BASE_DIR), "rb")))
                    transaction.save()
                    self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})

        # Release lock after accessing stay_still_arr
        # Remove after face_compare
        os.remove(temp_face_path)

    def face_process(self, temp_face_path):
        result = DeepFace.find(
            img_path=temp_face_path,
            db_path="C:/DriveD/Face recog website/mysite/face_recog/faces",
            model_name='VGG-Face',
            enforce_detection=False
        )
        self.face_compare(result, temp_face_path)

    def run_recognition(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            rgb_small_frame = small_frame[:, :, ::-1]
            faces = face_cascade.detectMultiScale(rgb_small_frame, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
            temp_dir = 'transaction_img'

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                face_image = frame[y:y+h, x:x+w]

                with tempfile.NamedTemporaryFile(suffix='.jpg', dir=temp_dir, delete=False) as temp_face_file:
                    temp_face_path = temp_face_file.name
                    cv2.imwrite(temp_face_path, face_image)
                    self.thread_pool.submit(self.face_process, temp_face_path)

            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()
