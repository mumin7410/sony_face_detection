# For x = s.split('/')[<number>] if in production use 3 else you need to justify
import cv2
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
from django.http import StreamingHttpResponse
import requests
from dotenv import load_dotenv

load_dotenv('.env')

class FaceRecognition:
    def __init__(self):
        self.stay_still_arr = []
        self.stay_still_arr_stranger = []
        self.stay_still_lock = threading.Lock()  # Lock for synchronization
        self.thread_pool = ThreadPoolExecutor(max_workers=1)

    def send_data_to_api(self, data, temp_face_path):
        print("send_data_to_api")
        api_url = f'{os.getenv("SERVER")}/api/addTransaction'  # Replace with your API endpoint URL
        files = {'Image': open(temp_face_path, 'rb')}
        response = requests.post(api_url, data=data, files=files)
        if response.status_code == 201:  # Assuming your API returns 201 for success
            print("Data sent successfully")
        else:
            print("Failed to send data:", response.status_code)

    def face_compare(self, result, temp_face_path,time,st):
        if len(result[0]) == 0:
            print('not found!!!')
            pass
        else:
            s = result[0]['identity'][0]
            print(s)
            x = s.split('/')[3]
            EmployeeID = x.split('_')[0] #EmpID
            Name = x.split('_')[1]

            EmployeeID = EmployeeID.replace(':', '')
            Name = Name.replace(':', '')

            print(f'EmployeeID------>{EmployeeID}')
            print(f'Name------>{Name}')

            # Acquire lock before accessing stay_still_arr
            with self.stay_still_lock:
                employee_in_arr = False
                for item in self.stay_still_arr:
                    if item['EmployeeID'] == EmployeeID:
                        employee_in_arr = True
                        time_difference = time - datetime.strptime(item['DateTime'], '%Y-%m-%d %H:%M:%S')
                        if time_difference.total_seconds() > 300:
                            # post data
                            # transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=time.strftime('%Y-%m-%d %H:%M:%S'), CameraNo=int(os.environ.get('CAMERA_VALUE', 1)), Image=File(open(Path(temp_face_path).relative_to(settings.BASE_DIR), "rb")))
                            # transaction.save()
                            data = {
                                'EmpID': EmployeeID,
                                'Name': Name,
                                'DateTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'CameraNo': int(os.getenv('CAMERA_NUMBER')),
                            }
                            self.send_data_to_api(data, temp_face_path)
                            self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': time.strftime('%Y-%m-%d %H:%M:%S')})
                if not employee_in_arr:
                    # post data
                    # transaction = Transaction(EmployeeID=EmployeeID, Name=Name, DateTime=time.strftime('%Y-%m-%d %H:%M:%S'), CameraNo=int(os.environ.get('CAMERA_VALUE', 1)), Image=File(open(Path(temp_face_path).relative_to(settings.BASE_DIR), "rb")))
                    # transaction.save()
                    data = {
                        'EmpID': EmployeeID,
                        'Name': Name,
                        'DateTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'CameraNo': int(os.getenv('CAMERA_NUMBER')),
                    }
                    self.send_data_to_api(data, temp_face_path)
                    self.stay_still_arr.append({'EmployeeID': EmployeeID, 'Name': Name, 'DateTime': time.strftime('%Y-%m-%d %H:%M:%S')})

        # Release lock after accessing stay_still_arr
        # Remove after face_compare
        os.remove(temp_face_path)
        et=datetime.now()
        print("total time consumeed ---->", (et-st).total_seconds())

    def face_process(self, temp_face_path):
        st = datetime.now()
        result = DeepFace.find(
            img_path=temp_face_path,
            db_path="face_recog/faces",
            model_name='VGG-Face',
            enforce_detection=False
        )
        time = timezone.now()
        self.face_compare(result, temp_face_path,time,st)

    def run_recognition(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)

        def generate():
            while True:
                ret, frame = cap.read()
                small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
                rgb_small_frame = small_frame[:, :, ::-1]
                faces = face_cascade.detectMultiScale(rgb_small_frame, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
                temp_dir = 'transaction_img'
                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face_image = frame[y:y+h, x:x+w]

                    with tempfile.NamedTemporaryFile(suffix='.jpg', dir=temp_dir, delete=False) as temp_face_file:
                        temp_face_path = temp_face_file.name
                        cv2.imwrite(temp_face_path, face_image)
                        self.thread_pool.submit(self.face_process, temp_face_path)

                # Encode the frame and yield it for streaming
                _, jpeg = cv2.imencode('.jpg', frame)
                frame_bytes = jpeg.tobytes()
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        response = StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
        return response


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()
