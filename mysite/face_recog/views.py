from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import recog
from .models import Member,Transaction
from .serializers import MemberSerializer,TransactionSerializer
from django.http import StreamingHttpResponse
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import cv2
# Create your views here.


@api_view(['GET'])
def getMembers(request):
    Blog = Member.objects.all()
    serializer = MemberSerializer(Blog, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTransaction(request):
    Blog = Transaction.objects.all()
    serializer = TransactionSerializer(Blog, many=True)
    return Response(serializer.data)

def index(request):
    fr = recog.FaceRecognition()
    return fr.run_recognition()

@api_view(['POST'])
def upload_emp_image(request):
    if request.method == 'POST':
        # Get the image file from the request
        image_file = request.FILES.get('image')

        # Get the EmpName and EmpId from the request
        EmpName = request.POST.get('EmpName')
        EmpId = request.POST.get('EmpId')

        # Construct the directory path
        directory_path = os.path.join('face_recog', 'faces', str(EmpId))

        # Remove the representations_vgg_face.pkl file if it exists
        pkl_file_path = os.path.join('face_recog', 'faces', 'representations_vgg_face.pkl')
        if os.path.exists(pkl_file_path):
            os.remove(pkl_file_path)

        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Get the latest number of files in the directory
        latest_file_number = len(os.listdir(directory_path))

        # Construct the file name
        file_name = f"{EmpId}_{EmpName}_{latest_file_number + 1}.jpg"

        # Construct the full file path
        file_path = os.path.join(directory_path, file_name)

        # Save the image file to the specified path
        fs = FileSystemStorage(location=directory_path)
        fs.save(file_name, image_file)

        return JsonResponse({'message': 'Image uploaded successfully', 'file_path': file_path})
    else:
        return JsonResponse({'error': 'Bad request. POST method expected'}, status=400)


