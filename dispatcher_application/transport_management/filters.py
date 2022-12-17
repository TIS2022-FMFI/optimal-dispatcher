import django_filters
from .models import *
from django_filters import *
from django import forms
        
class TransportFilter(django_filters.FilterSet):
    #my_data = BooleanFilter(label="Only my data", lookup_expr='exact',field_name="owner_id",widget=forms.CheckboxInput(attrs={'class': 'form-check-input',"type":"checkbox"}))
    from_id = CharFilter(field_name="from_id", lookup_expr="icontains", label="From:")
    departure_time = DateTimeFilter(field_name="departure_time",label="Date:",widget=forms.TextInput(attrs={"type":"date"}))
    class Meta:
        model = Transportations
        fields = ["from_id","departure_time","owner_id"]