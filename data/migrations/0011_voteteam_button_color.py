# Generated by Django 5.0.3 on 2024-03-28 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_remove_voteteamuser_vote_voteteamuser_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteteam',
            name='button_color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]