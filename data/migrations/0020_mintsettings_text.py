# Generated by Django 5.0.3 on 2024-04-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_mintsettings_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='mintsettings',
            name='text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
