# Generated by Django 4.1.3 on 2022-11-10 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0009_requestteam_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='section',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
