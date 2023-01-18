import datetime
from django.db import connections
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from datetime import datetime
from .models import Location, Transportations
from user_management.models import MyUser
from access_management.models import UserBranchAccess, GroupBranchAccess, UserGroupAccess
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from django.db import IntegrityError
from django.core import serializers

from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
import re

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decorators = [login_required()]


@method_decorator(decorators, name="dispatch")
class ListTransportationsView(ListView):
    model = Transportations
    template_name = 'transport_management/transportation_list.html'
    paginate_by = 25


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtered_by = ''
        self.search_val = { 'owner' : '', 'from' : '', 'departure' : '', 'arrival' : ''}


    def get_queryset(self): 
        self.user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access'])}

        search_owner_value = self.request.GET.get('owner')
        search_from_value = self.request.GET.get('from_location')
        search_departure_value = self.request.GET.get('departure_date')
        search_arrival_value = self.request.GET.get('arrival_date')
        
        if (self.is_empty_filter(search_owner_value) and self.is_empty_filter(search_from_value) and 
            self.is_empty_filter(search_departure_value) and self.is_empty_filter(search_arrival_value)):
            return Transportations.objects.filter(owner_id__branch__in=self.user_branch_access)
           
        search_owner_value = search_owner_value.strip()
        search_from_value = search_from_value.strip()
        search_departure_value = search_departure_value.strip()
        search_arrival_value = search_arrival_value.strip()

        self.filtered_by = f'&owner={search_owner_value}&from-location={search_from_value}&departure-date={search_departure_value}&arrival-date={search_arrival_value}'
        self.search_val = {
            'owner' : search_owner_value,
            'from' : search_from_value, 
            'departure' : search_departure_value, 
            'arrival' : search_arrival_value
        }
        
        # extract locations ids from QuerySet
        locations = self.get_location_ids(search_from_value)

        if len(locations) < 1:
            locations = ''
        search_string = f"{search_owner_value} {locations} {search_departure_value} {search_arrival_value}"

        result = self.get_transportations_queryset(search_string)
        return result


    def is_empty_filter(self, input_value):
        if input_value is None or input_value.strip() == '':
            return True
        return False


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
        context['owners_list'] = MyUser.objects.filter(branch_id__in=self.user_branch_access)
        context['location_list'] = Location.objects.all()
        return context


    def get_location_ids(self, input):
        pattern = r"^([0-9]{5,10})[, -;]([A-Za-z]{2,70})[, -;]([A-Za-z]{2,3})$"
        if not(re.match(pattern, input)):
            return Location.objects.none()

        location_groups = re.search(pattern, input)
        formated_location = f'{location_groups.group(1)} {location_groups.group(2)} {location_groups.group(3)}'

        locations = Location.objects.annotate(
            search=SearchVector('zip_code', 'city', 'country'),
            ).filter(search=formated_location).values_list('id')

        return {pk for pk in locations}


    def get_transportations_queryset(self, serach_string):
        result = Transportations.objects.annotate(
                search=SearchVector('owner_id__email', 'from_id', 'departure_time', 'arrival_time'),
                ).filter(
                    Q(search=serach_string) & 
                    Q(owner_id__branch__in=self.user_branch_access)
                )
        return result
    


@method_decorator(decorators, name="dispatch")
class TransportationAddView(View):
    template = "transport_management/transportation_form.html"

    def get(self, request):
        location_list = Location.objects.all()
        context = {'location_list': location_list, 'button_text': 'Add'}
        return render(request, self.template, context)


    def post(self, request):
        from_location = request.POST['from_id']
        to_location = request.POST['to_id']
        departure_date = request.POST['departure_date']
        departure_time = request.POST['departure_time']
        arrival_date = request.POST['arrival_date']
        arrival_time = request.POST['arrival_time']
        ldm = request.POST['ldm']
        weight = request.POST['weight']
        info = request.POST['info']

        departure = datetime.combine(parse_date(departure_date), parse_time(departure_time))
        arrival = datetime.combine(parse_date(arrival_date), parse_time(arrival_time))

        
        # error_message = check_data(from_id, to_id, departure, arrival)
        # if error_message != "":
        #     context = {'from_id': from_location, 'to_id': to_location, 'departure_date': departure_date,
        #                'departure_time': departure_time, 'arrival_date': arrival_date, 'arrival_time': arrival_time,
        #                'ldm': ldm, 'weight': weight, 'info': info, 'error_message': error_message, 'button_text': 'Add'}
        #     return render(request, self.template, context)

        try:
            with transaction.atomic(): 
                from_location = get_location(from_location.split(","))
                to_location = get_location(to_location.split(","))
                Transportations.objects.create(
                    owner_id=self.request.user, 
                    from_id=from_location, 
                    to_id=to_location, 
                    departure_time=departure, 
                    arrival_time=arrival, 
                    ldm=ldm, 
                    weight=weight, 
                    info=info
                )
                # insert_transport(self.request.user.id, from_id, to_id, departure, arrival, ldm, weight, info)
        except IntegrityError:
            ...
        return redirect('transportation-add')


    ...
@method_decorator(decorators, name="dispatch")
class TransportationUpdateView(UpdateView):
    model = Transportations
    template_name = "transport_management/transportation_form.html"
    success_url = 'transportation-list'
    fields = [
        'from_id', 'to_id', 'departure_time','arrival_time','ldm','weight','info'
    ]

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = 'Edit'
        return context

    def get_queryset(self): 
        user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access'])}
        pk = self.kwargs['pk']
        transport =  Transportations.objects.filter(Q(id=pk) & Q(owner_id__branch__in=user_branch_access))
        return transport

  



def get_location(location):
    """
    returns id number of the location parameter
    if it doesn't already exist, creates a new location in the known_locations_management_location table
    """
    try:
        return Location.objects.get(zip_code=location[0], city=location[1], country=location[2])
    except ObjectDoesNotExist:
        return Location.objects.create(zip_code=location[0], city=location[1], country=location[2])
    

def insert_transport(user_id, from_id, to_id, departure, arrival, ldm, weight, info):
    cursor = connections['default'].cursor()
    cursor.execute(
        "INSERT INTO transport_management_transportations(owner_id_id,from_id_id,to_id_id,departure_time, arrival_time, ldm, weight, info) "
        "VALUES( %s, %s, %s, %s, %s, %s, %s, %s)",
        [user_id, from_id, to_id, departure, arrival, ldm, weight, info])


def update_transport(transportation_id, from_id, to_id, departure, arrival, ldm, weight, info):
    cursor = connections['default'].cursor()
    cursor.execute(
        "UPDATE transportations "
        "SET from_id = %s, to_id= %s, departure= %s, arrival= %s, ldm= %s, weight= %s, info= %s) "
        "WHERE id = %s",
        [from_id, to_id, departure, arrival, ldm, weight, info, transportation_id])


def check_data(from_id, to_id, departure, arrival):
    error_message = ""
    if from_id == -1 or to_id == -1 or from_id == to_id:
        error_message = "Wrong location input"

    if departure >= arrival:
        if error_message != "":
            error_message += '\n'
        error_message += "Departure cannot be later than arrival"

    return error_message


class TransportationDetailView(DetailView):
    model = Transportations
    template_name = 'transport_management/transportation_detail.html'

    def get_queryset(self): 
        user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access'])}
        pk = self.kwargs['pk']
        transport = Transportations.objects.filter(Q(id=pk) & Q(owner_id__branch__in=user_branch_access))
        return transport

    