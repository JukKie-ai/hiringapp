# Generated by Django 3.1.14 on 2022-10-22 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_requestteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.IntegerField(default=0),
        ),
    ]
