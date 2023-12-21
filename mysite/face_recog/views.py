from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import recog
from .models import Member,Transaction
from .serializers import MemberSerializer,TransactionSerializer
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
    fr.run_recognition()
    # member = Member.objects.get(Name="Mumin")
    return HttpResponse("Index")