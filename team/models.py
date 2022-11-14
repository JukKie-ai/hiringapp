from email.policy import default
from django.db import models

COURSE_CHOICES = [('Information Technology', 'Information Technology'), ('Computer Science', 'Computer Science')]

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    course = models.CharField(choices=COURSE_CHOICES, max_length=50, null=True)
    status = models.BooleanField(default=False)

class Admin(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)

class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    founder = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField()
    section = models.CharField(max_length=10, null=True)
    members = models.IntegerField(default=0)
    max_members = models.IntegerField()

class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True)


class RequestTeam(models.Model):
    requestTeamID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    teamID = models.ForeignKey(Team, on_delete=models.CASCADE)
    reason = models.TextField(null=True)

