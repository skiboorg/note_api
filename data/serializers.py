from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'



class NoteSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Note
        fields = '__all__'



class DaoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaoCode
        fields = '__all__'

class SentCapSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()
    class Meta:
        model = SentCaptcha
        fields = ['uid','image']
    def get_image(self,obj):
        return obj.captcha.image.url

class DaoRequestSerializer(serializers.ModelSerializer):
    code = DaoCodeSerializer(read_only=True)
    class Meta:
        model = DaoRequest
        fields = '__all__'




