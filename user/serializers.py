
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings

from django.contrib.auth.tokens import default_token_generator

# from .services import send_email




import logging
logger = logging.getLogger(__name__)
class UserClaimUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClaimUpgrade
        fields = '__all__'
class UserCoinsUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoinsUpgrade
        fields = '__all__'
class ClaimUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimUpgrade
        fields = '__all__'

class CoinUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinUpgrade
        fields = '__all__'
class TransactionSerializer(serializers.ModelSerializer):
    to_user = serializers.SerializerMethodField()
    from_user = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = '__all__'

    def get_to_user(self,obj):
        return obj.to_user.uid

    def get_from_user(self, obj):
        return obj.from_user.uid

class UserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'twitter',
            'wallet'
        ]

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    income = TransactionSerializer(many=True, read_only=True)
    outcome = TransactionSerializer(many=True, read_only=True)
    coins_add = serializers.SerializerMethodField()
    limit_add= serializers.SerializerMethodField()
    total_claimes= serializers.SerializerMethodField()
    claim_upgrades = UserClaimUpgradeSerializer(many=True, read_only=True)
    coin_upgrades = UserCoinsUpgradeSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'income',
            'outcome',
            'email',
            'twitter',
            'wallet',
            "avatar",
            "is_in_wl",
            "code",
            "balance",
            'can_claim',
            'uid',
            'claims',
            'coins_add',
            'limit_add',
            'total_claimes',
            'claim_upgrades',
            'coin_upgrades'
        ]

        extra_kwargs = {
            'password': {'required': False},

        }

    def get_total_claimes(self, obj):
        result = 3
        for upgrade in obj.claim_upgrades.all():
            print(upgrade)
            result += upgrade.claim_upgrade.claim_add
        return result
    def get_coins_add(self,obj):
        result = 0
        for upgrade in obj.coin_upgrades.all():
            print(upgrade)
            result += upgrade.coin_upgrade.click_add
        return result


    def get_limit_add(self,obj):
        result = 0
        for upgrade in obj.coin_upgrades.all():
            result += upgrade.coin_upgrade.limit_add
        return result


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR,
        "invalid_code": 'Invalid code',
        "code_used": 'code was used',
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'email',
            'password',
            'code',
            'twitter',
            'wallet',

        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")


        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            print(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):

        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        print(validated_data)
        code = validated_data.get('code')
        code_in_db = None
        try:
            code_in_db = Code.objects.get(code=code)
        except:
            self.fail("invalid_code")
        if code_in_db:

            if not code_in_db.is_unlimited and code_in_db.is_used:
                self.fail("invalid_code")
            else:
                if code_in_db.use_number > 0:
                    code_in_db.use_number -= 1
                    code_in_db.save()
                else:
                    code_in_db.is_used = True
                    code_in_db.save()

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            user.is_active = True
            user.save(update_fields=["is_active"])
        return user


