# Generated by Django 5.1.3 on 2024-12-26 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0008_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='body',
            field=models.CharField(max_length=500),
        ),
    ]
