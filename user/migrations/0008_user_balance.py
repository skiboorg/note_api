# Generated by Django 5.0.1 on 2024-03-21 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_fk_wl_1_user_fk_wl_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]