from .models import *
from django_filters import django_filters, CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter

class GroupFilter(django_filters.FilterSet):
    name = ModelChoiceFilter(label="Group name:", queryset=Group.objects.all())
    class Meta:
        model = Group
        fields = ["name"]