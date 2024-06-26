import json

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from data.models import Note, SentCaptcha, MintSettings
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
    permission_classes = [IsAuthenticated]
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

class BuyUpgrade(APIView):
    def post(self, request):
        result = {'s':False,'m':''}
        print(request.data)
        upgrade_type = request.data['upgrade']
        item_id = request.data['id']
        user = request.user
        if upgrade_type == 'claim':
            upgrade = ClaimUpgrade.objects.get(id=item_id)
            if user.balance < upgrade.price:
                result['m'] = 'No balance'
                return Response(result,status=200)
            qs = user.claim_upgrades.all().filter(claim_upgrade_id=item_id)
            if qs.exists():
                result['m'] = 'Already upgraded'
                return Response(result, status=200)
            user.balance -= upgrade.price
            user.save()
            UserClaimUpgrade.objects.create(user=user,claim_upgrade_id=item_id)
            result['s'] = True
            result['m'] = 'Success'
            return Response(result, status=200)
        if upgrade_type == 'coin':
            upgrade = CoinUpgrade.objects.get(id=item_id)
            if user.balance < upgrade.price:
                result['m'] = 'No balance'
                return Response(result,status=200)
            qs = user.coin_upgrades.all().filter(coin_upgrade_id=item_id)
            if qs.exists():
                result['m'] = 'Already upgraded'
                return Response(result, status=200)
            user.balance -= upgrade.price
            user.save()
            UserCoinsUpgrade.objects.create(user=user,coin_upgrade_id=item_id)
            result['s'] = True
            result['m'] = 'Success'
            return Response(result, status=200)
        return Response()


class Test(APIView):
    def get(self, request):
        # codes = Code.objects.all()
        # for code in codes:
        #     code.code = code.code.upper()
        #     code.save()
        from .tasks import resetClaim
        resetClaim.delay()
        return Response()
class TxHistory(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    pagination_class = Pagination

class SaveForm(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = create_random_string(num=8)
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
        if user.claims == 0:
            return Response({'s': False,'m':'Out of limit'}, status=200)
        if not user.can_claim:
            return Response({'s': False,'m':'Blocked'}, status=200)
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
            return Response({'s':False,'m':'Captcha error! Coins have been burn3d.'},status=200)
        captcha = sentCap[0]
        if captcha.captcha.code != request.data['code']:
            user.errors += 1
            user.save()
            captcha.delete()
            return Response({'s': False,'m':'Captcha error! Coins have been burn3d.'}, status=200)

        user.balance += request.data['amount']
        ClaimHistory.objects.create(user=user, amount=request.data['amount'])
        user.claims -= 1
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

class CheckWalletWl(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        print(request.data)
        result = {}
        serializer = WalletSerializer
        wallets = Wallet.objects.filter(wallet=request.data['wallet'])
        if wallets.exists():
            result = serializer(wallets.first()).data
            result['success'] = True
        else:
            result = {'success': False}

        return Response(result,status=200)

class ClaimUpgrades(generics.ListAPIView):
    queryset = ClaimUpgrade.objects.all()
    serializer_class = ClaimUpgradeSerializer

class CoinUpgrades(generics.ListAPIView):
    queryset = CoinUpgrade.objects.all()
    serializer_class = CoinUpgradeSerializer


class Mintt(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        result = {'success': False}
        mints = Mint.objects.filter(user=request.user)
        if mints.exists():
            serializer = MintWalletSerializer(mints.first(), many=False)
            result = {'success': True, "info": serializer.data}
        return Response(result, status=200)

    def post(self,request,*args,**kwargs):
        settings, _ = MintSettings.objects.get_or_create(id=1)
        print(request.data)
        user = request.user
        result = {}
        i_send = request.data.get("uid",False)
        priority = request.data.get("priority")
        need_balance = 0
        if priority == "Low":
            need_balance += 0
        elif priority == "Medium":
            need_balance += 300
        elif priority == "High":
            need_balance += 3000
        else:
            need_balance += 666879789
        if i_send:
            mint = Mint.objects.get(wallet=request.data['wallet'], checked=True)
            mint.send = True
            mint.save()
            result = {'success': True, 'message': 'Bot checking ur payment and confirming it'}
        else:
            if not settings.public:
                wallets_in_wl = None
                if settings.wl:
                    wallets_in_wl = Wallet.objects.filter(wallet=request.data['wallet'], wl=True)
                if settings.wl1:
                    wallets_in_wl = Wallet.objects.filter(wallet=request.data['wallet'], wl1=True)
                if not wallets_in_wl.exists():
                    result = {'success': False, 'message': 'Your receive wallet is not on the list. please wait for next wave'}
                    return Response(result, status=200)
            if user.balance < need_balance:
                result = {'success': False, 'message': 'not enough coins'}
                return Response(result, status=200)
            user.balance -= need_balance
            user.save()

            wallet_used = Mint.objects.filter(wallet=request.data['wallet'])
            if wallet_used.exists():
                result = {'success': False, 'message': 'This wallet has already been used. If this is your wallet, please contact support by clicking the "Create Ticket" button below.'}
                return Response(result, status=200)
            else:
                Mint.objects.create(user=user, wallet=request.data['wallet'],priority=priority, send_wallet=request.data['send_wallet'], checked=True)
            result = {'success': True, 'message': 'Success'}


        return Response(result,status=200)