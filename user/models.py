import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from datetime import timedelta
# from .tasks import send_email

import logging
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Code(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    is_used = models.BooleanField(default=False, null=False)
    is_unlimited = models.BooleanField(default=False, null=False)
    use_number = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return f'{self.code}'

class PasswordForm(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    is_done = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'{self.email}'


class User(AbstractUser):
    username = None
    firstname = None
    lastname = None
    uid = models.CharField('user uid           ',max_length=255, blank=True, null=True, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    wallet = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.FileField(upload_to='usr/ava',blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True)
    is_in_wl = models.BooleanField(default=False, blank=True)
    fk_wl_1 = models.BooleanField(default=False, blank=True)
    fk_wl_2 = models.BooleanField(default=False, blank=True)
    errors = models.IntegerField(default=0)
    blocked = models.DateTimeField(blank=True,null=True)
    can_claim = models.BooleanField(default=True, blank=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.email} | {self.uid}'



class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcome')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income')
    amount = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



