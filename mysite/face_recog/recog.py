from django.utils import timezone
from datetime import datetime
import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from .models import Transaction
from django.core.files import File
import os
import threading
import tempfile
from pathlib import Path
from django.conf import settings


class FaceRecognition:
    def __init__(self):
        self.stay_still_arr = []

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
        # Remove after face_compare
        os.remove(temp_face_path)


    def run_recognition(self):
        # Load the pre-trained MTCNN model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Capture video from the default camera (use 0)
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Detect faces using MTCNN
            faces = face_cascade.detectMultiScale(rgb_small_frame, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
            temp_dir = 'transaction_img'
            for (x, y, w, h) in faces:
                # Capture and save the face region as an image
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                face_image = frame[y:y+h, x:x+w]

                with tempfile.NamedTemporaryFile(suffix='.jpg',dir=temp_dir, delete=False) as temp_face_file:
                    temp_face_path = temp_face_file.name
                    cv2.imwrite(temp_face_path, face_image)
                    # Perform facial recognition using DeepFace on the captured face region
                    result = DeepFace.find(
                        img_path=temp_face_path,  # Use the captured face region directly
                        db_path="C:/DriveD/Face recog website/mysite/face_recog/faces",
                        model_name='VGG-Face',
                        enforce_detection=False
                    )
                    # Use threading to perform face comparison
                    thread = threading.Thread(target=self.face_compare, args=(result,temp_face_path))
                    thread.start()

            # Display the frame
            cv2.imshow('Face Detection', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

