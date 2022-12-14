# Generated by Django 3.1.14 on 2022-10-19 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.CharField(choices=[('Information Technology', 'Information Technology'), ('Computer Science', 'Computer Science')], max_length=50)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='team.team')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.user')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='founder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.user'),
        ),
    ]
