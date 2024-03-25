from django.db import models
from uuid import uuid4
class Note(models.Model):
    uid = models.CharField(max_length=20,blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    wallet = models.TextField(blank=True,null=True)
    twitter = models.CharField(max_length=100,blank=True,null=True)
    only_twitter = models.BooleanField(default=False,null=False)
    is_wl = models.BooleanField(default=False,null=False)
    is_viewed = models.BooleanField(default=False,null=False)
    is_forever = models.BooleanField(default=False,null=False)

    def __str__(self):
        return f'{self.uid}'



class Link(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)


class Image(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True, related_name='images')
    file = models.FileField(upload_to='images',blank=True,null=True)


class DaoCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    is_used = models.BooleanField(default=False, null=False)
    # is_unlimited = models.BooleanField(default=False, null=False)
    # use_number = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return f'{self.code}'

class DaoRequest(models.Model):
    code = models.ForeignKey(DaoCode, on_delete=models.CASCADE, blank=True, null=True)
    twitter = models.CharField(max_length=255,blank=True,null=True)
    dao_twitter = models.CharField(max_length=255,blank=True,null=True)
    file = models.FileField(upload_to='requests',blank=True,null=True)

    def __str__(self):
        return f'{self.code} | {self.twitter}'


class Captcha(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to='captchas',blank=True,null=True)

    def __str__(self):
        return f'{self.code}'


class SentCaptcha(models.Model):
    captcha = models.ForeignKey(Captcha, on_delete=models.CASCADE, blank=True, null=True)
    uid = models.CharField(max_length=255, default=uuid4(), null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
