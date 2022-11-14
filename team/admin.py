from urllib.request import Request
from django.contrib import admin
from .models import RequestTeam, User, Team, Student, Admin

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Student)
admin.site.register(RequestTeam)
admin.site.register(Admin)