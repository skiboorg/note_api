from rest_framework import serializers
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


class DaoRequestSerializer(serializers.ModelSerializer):
    code = DaoCodeSerializer(read_only=True)
    class Meta:
        model = DaoRequest
        fields = '__all__'




