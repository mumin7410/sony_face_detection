from django.utils import timezone
from datetime import datetime
import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from .models import Transaction
from django.core.files import File
import os

class FaceRecognition:
    def __init__(self):
        self.stay_still_arr = []
    def run_recognition(self):
        # Load the pre-trained MTCNN model
        detector = MTCNN()

        # Capture video from the default camera (use 0)
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Detect faces using MTCNN
            faces = detector.detect_faces(rgb_small_frame)

            for face in faces:
                x, y, width, height = face['box']

                # Capture and save the face region as an image
                face_image = frame[y:y + height, x:x + width]
                cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
                
                # Perform facial recognition using DeepFace on the captured face region
                result = DeepFace.find(
                    img_path=face_image,  # Use the captured face region directly
                    db_path="C:/DriveD/Face recog website/mysite/face_recog/faces",
                    model_name='VGG-Face',
                    enforce_detection=False
                )

                if result[0].empty:
                    name = 'Stranger !!!'
                    face_image_path = os.path.join(MEDIA_ROOT, f'{EmployeeID}_{Name}.jpg')
                    cv2.imwrite(face_image_path, face_image)
                    # post data
                    transaction = Transaction(EmployeeID=0,Name=name,DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),CameraNo=1,Image=File(open(face_image_path, "rb")))
                    transaction.save()
                else:
                    s = result[0]['identity'][0]
                    x = s.split('/')[6]
                    EmployeeID = x.split('_')[0] #EmpID
                    Name = x.split('_')[1]
                    
                    employee_in_arr = False
                    for item in self.stay_still_arr:
                        if item['EmployeeID'] == EmployeeID:
                            employee_in_arr = True
                            time_difference = timezone.now() - datetime.strptime(item['DateTime'], '%Y-%m-%d %H:%M:%S')
                            if time_difference.total_seconds() > 300:
                                face_image_path = os.path.join(MEDIA_ROOT,f'{EmployeeID}_{Name}.jpg')
                                cv2.imwrite(face_image_path, face_image)
                                # post data
                                transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'), CameraNo=1, Image=File(open(face_image_path, "rb")))
                                transaction.save()
                                self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
                    if not employee_in_arr:
                        face_image_path = os.path.join(f'{EmployeeID}_{Name}.jpg')
                        cv2.imwrite(face_image_path, face_image)
                        # post data
                        transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=timezone.now().strftime('%Y-%m-%d %H:%M:%S'), CameraNo=1, Image=File(open(face_image_path, "rb")))
                        transaction.save()
                        self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})

            # Display the frame
            cv2.imshow('Face Detection', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

