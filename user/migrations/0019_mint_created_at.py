# Generated by Django 5.0.3 on 2024-04-16 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_mint'),
    ]

    operations = [
        migrations.AddField(
            model_name='mint',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]