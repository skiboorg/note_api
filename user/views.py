import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from data.models import Note

import logging
logger = logging.getLogger(__name__)



class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UpdateUser(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        instance = User.objects.get(email=request.data['email'])

        serializer = UserSerializer(instance,data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            obj.save()

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

class CheckWallet(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        result = {}

        try:
            note = Note.objects.get(wallet=request.data['wallet'])
            instance = User.objects.get(wallet=request.data['wallet'])
            instance.is_in_wl = True
            instance.save()
            result = {'success': True}
        except:
            result = {'success': False}

        return Response(result,status=200)