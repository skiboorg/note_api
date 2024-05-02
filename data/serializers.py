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






class MintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MintImage
        fields = '__all__'
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class MintSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MintSettings
        fields = '__all__'


class VoteTeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteTeamUser
        fields = '__all__'

class VoteTeamSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = VoteTeam
        fields = '__all__'

    def get_users(self,obj):
        print(obj.users.all())
        ids = []
        for user in obj.users.all():
            ids.append(user.user.uid)
        return ids

class VoteSerializer(serializers.ModelSerializer):
    teams = VoteTeamSerializer(many=True, read_only=True)
    class Meta:
        model = Vote
        fields = '__all__'

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'
