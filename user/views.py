import json

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from data.models import Note,SentCaptcha
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)
from .services import create_random_string
import settings
import datetime
from django.utils.timezone import now

from rest_framework.parsers import MultiPartParser

class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        if not user.uid:
            user.uid = f'{create_random_string()}-{create_random_string()}'
            user.save()
        if not user.can_claim:
            if now() >= user.blocked + datetime.timedelta(seconds=33):
                user.can_claim = True
                user.blocked = None
                user.save()
        return user


class MakeCodes(APIView):
    def get(self, request):
        users = User.objects.all()
        for user in users:
            user.uid = f'{create_random_string()}-{create_random_string()}'
            user.save()
        return Response(status=200)
class UpdateUser(APIView):
    #parser_classes = [MultiPartParser]
    def post(self,request,*args,**kwargs):
        # print(request.data)
        # print(request.data.get('email',None))
        # print(request.FILES.get('file'))
        instance = request.user #User.objects.get(email=request.data['email'])

        serializer = UserSaveSerializer(instance,data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            #obj.avatar  = request.FILES.get('file')
            obj.save()

        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

class Pagination(PageNumberPagination):
    page_size = 66
    page_size_query_param = 'page_size'
    max_page_size = 10000

class TxHistory(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    pagination_class = Pagination

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


class Send(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        result = {'success': True,"message":"successful sended"}
        print(request.data)
        to_user_qs = User.objects.filter(uid=request.data['to'])
        if not to_user_qs.exists():
            result = {'success': False, "message": "user uid not found"}
            return Response(result, status=200)
        to_user = to_user_qs.first()
        if to_user == request.user:
            result = {'success': False, "message": "user not found"}
            return Response(result, status=200)
        amount = int(request.data['amount'])
        amount_with_commission = amount+30
        if not request.user.balance >= amount_with_commission:
            result = {'success': False, "message": "not enough coins"}
            return Response(result, status=200)
        request.user.balance -= amount_with_commission
        request.user.save()
        to_user.balance += amount
        to_user.save()
        uid = f'DCx{create_random_string(num=16)}'
        Transaction.objects.create(uid=uid, from_user=request.user, to_user=to_user, amount=amount)
        return Response(result, status=200)


class Claim(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.data)
        user= request.user
        print(user)
        if not user.can_claim:
            return Response({'s': False}, status=200)
        if user.errors >= 99:
            user.can_claim = False
            user.errors = 0
            user.blocked = datetime.datetime.now()
            user.save()

        capUid = request.data['c']
        sentCap = SentCaptcha.objects.filter(uid=capUid) #,user=user
        if not sentCap.exists():
            user.errors += 1
            user.save()
            return Response({'s':False},status=200)
        captcha = sentCap[0]
        if captcha.captcha.code != request.data['code']:
            user.errors += 1
            user.save()
            captcha.delete()
            return Response({'s': False}, status=200)

        user.balance += request.data['amount']
        ClaimHistory.objects.create(user=user, amount=request.data['amount'])
        user.save()
        captcha.delete()
        return Response({'s':True},status=200)


class CrTxId(APIView):
    def get(self, request):
        all_tx = Transaction.objects.all()
        for tx in all_tx:
            tx.uid = f'DCx{create_random_string(num=16)}'
            tx.save()
        return Response(status=200)
class CheckWallet(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        result = {}

        try:
            note = Note.objects.get(wallet=request.data['wallet'])
            wall = User.objects.get(wallet=request.data['wallet'])
            instance = request.user #instance = User.objects.get(wallet=request.data['wallet'])
            instance.is_in_wl = True
            instance.save()
            result = {'success': True}
        except:
            result = {'success': False}

        return Response(result,status=200)