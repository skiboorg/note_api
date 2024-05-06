from .models import *
from datetime import datetime
from celery import shared_task
from user.models import User, Transaction


@shared_task
def calcStats():
    total_coins = 0
    total_tx_vol = 0
    all_tx = Transaction.objects.all()
    all_users = User.objects.all()
    for tx in all_tx:
        total_tx_vol += tx.amount
    for user in all_users:
        total_coins += user.balance
    stats,_ = Stats.objects.get_or_create(id=1)
    stats.total_coins = total_coins
    stats.total_tx_vol = total_tx_vol
    stats.save()

@shared_task
def checkVotes():
    votes = Vote.objects.filter(is_active=True)
    for vote in votes:
        if vote.time_left > 0:
            vote.time_left -= 1
        else:
            vote.is_active = False
        vote.save()

@shared_task
def mintTimer():
    settings = MintSettings.objects.get(id=1)
    if settings.time_left > 0:
        settings.time_left -= 1
        settings.save()
