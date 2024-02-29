import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from data.models import Note
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)
from .services import create_random_string
import settings

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

class SaveForm(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = create_random_string(False,8)
        result = {'success': True}
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            msg_html = render_to_string('notify.html', {'text':password})
            send_mail('Password reset', None, settings.SMTP_FROM, [user.email],
                      fail_silently=False, html_message=msg_html)
        except:
            result['success'] = False
        return Response(result, status=200)
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