from django.db.models import fields
import django_filters

from .models import *

class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = [
            'section',
        ]