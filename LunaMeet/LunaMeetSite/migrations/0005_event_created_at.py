# Generated by Django 5.1.3 on 2024-11-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LunaMeetSite', '0004_alter_photos_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
