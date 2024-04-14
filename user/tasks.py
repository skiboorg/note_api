
from celery import shared_task
from user.models import User


@shared_task
def resetClaim():
    users = User.objects.all()
    for user in users:
        claims = 3
        for claim_upgrade in user.claim_upgrades.all():
            claims += claim_upgrade.claim_upgrade.claim_add
        user.claims = claims
        user.save()

