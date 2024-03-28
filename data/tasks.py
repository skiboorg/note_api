from .models import *
from datetime import datetime
from celery import shared_task


@shared_task
def checkVotes():
    votes = Vote.objects.filter(is_active=True)
    for vote in votes:
        if vote.time_left > 0:
            vote.time_left -= 1
        else:
            vote.is_active = False
        vote.save()

