from .models import *
from django_filters import django_filters, CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter

class GroupFilter(django_filters.FilterSet):
    group_name = CharFilter(field_name="group_name", lookup_expr="icontains", label="Group:")
    branch_id = ModelChoiceFilter(label="Branch:", queryset=Branch.objects.all())
    class Meta:
        model = Groups
        fields = ["group_name","branch_id"]