import datetime
from django.db import connections
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from datetime import datetime
from .models import Location, Transportations
from access_management.models import UserBranchAccess, GroupBranchAccess, UserGroupAccess
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from django.db import IntegrityError
from django.core import serializers

from django.views.generic.list import ListView
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


    def get_queryset(self): 
        search_from_value = self.request.GET.get('from-location')
        search_departure_value = self.request.GET.get('departure-date')
        search_arrival_value = self.request.GET.get('arrival-date')
        
        self.user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access']) }
        self.filtered_by = ''
        self.search_val = { 'from' : '', 'departure' : '', 'arrival' : ''}
        result = Transportations.objects.none()

        if (search_from_value is None and search_departure_value is None and search_arrival_value is None or 
            search_from_value.strip() == '' and search_departure_value.strip() == '' and search_arrival_value.strip() == ''):
           return Transportations.objects.filter(owner_id__branch__in=self.user_branch_access)
           

        search_from_value = search_from_value.strip()
        search_departure_value = search_departure_value.strip()
        search_arrival_value = search_arrival_value.strip()

        self.filtered_by = f'&from-location={search_from_value}&departure-date={search_departure_value}&arrival-date={search_arrival_value}'
        self.search_val = {
            'from' : search_from_value, 
            'departure' : search_departure_value, 
            'arrival' : search_arrival_value
        }
        
        locations = {i for i in self.get_location_ids(search_from_value)}
        result = self.get_transportations_queryset(locations, search_departure_value, search_arrival_value)
        return result


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_by
        context['search_value'] = self.search_val
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
        return locations


    def get_transportations_queryset(self, from_ids, departure, arrival):
        if len(from_ids) < 1:
            from_ids = ''
        result = Transportations.objects.annotate(
                search=SearchVector('from_id', 'departure_time', 'arrival_time'),
                ).filter(search=f"{from_ids} {departure} {arrival}").filter(owner_id__branch__in=self.user_branch_access) 
        return result
    


@method_decorator(decorators, name="dispatch")
class TransportationView(View):
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




# @method_decorator(decorators, name="dispatch")
# class EditTransportationView(View):
#     template = "transport_management/transportation_form.html"

#     def get(self, request, **kwargs):
#         transportation = Transportations.objects.get(id=kwargs["pk"])
#         context = {'from_id': Location.objects.get(id=transportation.from_id_id),
#                    'to_id': Location.objects.get(id=transportation.to_id_id),
#                    'departure_date': str(transportation.departure_time.date()),
#                    'departure_time': str(transportation.departure_time.time()),
#                    'arrival_date': str(transportation.arrival_time.date()),
#                    'arrival_time': str(transportation.arrival_time.time()),
#                    'ldm': transportation.ldm,
#                    'weight': transportation.weight,
#                    'info': transportation.info,
#                    'button_text': 'Edit'}

#         return render(request, self.template, context)

#     def post(self, request, **kwargs):
#         transportation_id = kwargs["pk"]

#         from_location = request.POST['from_id']
#         to_location = request.POST['to_id']
#         departure_date = request.POST['departure_date']
#         departure_time = request.POST['departure_time']
#         arrival_date = request.POST['arrival_date']
#         arrival_time = request.POST['arrival_time']
#         ldm = request.POST['ldm']
#         weight = request.POST['weight']
#         info = request.POST['info']

#         from_id = get_location_id(from_location.split(","))
#         to_id = get_location_id(to_location.split(","))

#         departure = datetime.combine(parse_date(departure_date), parse_time(departure_time))
#         arrival = datetime.combine(parse_date(arrival_date), parse_time(arrival_time))

#         error_message = check_data(from_id, to_id, departure, arrival)
#         if error_message != "":
#             context = {'from_id': from_location, 'to_id': to_location, 'departure_date': departure_date,
#                        'departure_time': departure_time, 'arrival_date': arrival_date, 'arrival_time': arrival_time,
#                        'ldm': ldm, 'weight': weight, 'info': info, 'error_message': error_message, 'button_text': 'Add'}
#             return render(request, self.template, context)

#         update_transport(transportation_id, from_id, to_id, departure, arrival, ldm, weight, info)
#         return redirect('/transports')


def get_location(location):
    """
    returns id number of the location parameter
    if it doesn't already exist, creates a new location in the known_locations_management_location table
    """
    try:
        return Location.objects.get(zip_code=location[0], city=location[1], country=location[2])
    except ObjectDoesNotExist:
        return Location.objects.create(zip_code=location[0], city=location[1], country=location[2])
    

    # new_location = Location()
    # new_location.zip_code = location[0]
    # new_location.city = location[1]
    # new_location.country = location[2]
    # new_location.save()

    # try:
    #     return Location.objects.get(zip_code=location[0], city=location[1], country=location[2]).id
    # except IndexError:
    #     return -1
    # except ObjectDoesNotExist:
    #     if len(location[0]) > 10 or len(location[1]) > 70 or len(location[2]) > 4:
    #         return -1

    #     new_location = Location()
    #     new_location.zip_code = location[0]
    #     new_location.city = location[1]
    #     new_location.country = location[2]
    #     new_location.save()
    #     return new_location.id


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
