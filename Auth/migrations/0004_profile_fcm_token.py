# Generated by Django 5.1.3 on 2025-01-05 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fcm_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
