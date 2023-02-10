from django.db import connections
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time

from django.http import Http404

from django.http import HttpResponseRedirect
from django.views.generic import FormView
from .forms import CreateTransportForm, UpdateTransportForm

from .models import Location, Transportations
from user_management.models import MyUser
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from django.db import IntegrityError
from django.core import serializers

from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.views.generic.base import RedirectView

from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.db import connection
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
        self.search_val = {'owner': '', 'from': '', 'departure': '', 'arrival': ''}


    def get_queryset(self):
        self.user_branch_access = {obj.object for obj in
                                   serializers.deserialize("json", self.request.session['logged_in_user_access'])}

        search_owner_value = self.request.GET.get('owner') or ''
        search_from_value = self.request.GET.get('from-location') or ''
        search_departure_value = self.request.GET.get('departure-date') or ''
        search_arrival_value = self.request.GET.get('arrival-date') or '' 

        if (self.is_empty_filter(search_owner_value) and self.is_empty_filter(search_from_value) and 
            self.is_empty_filter(search_departure_value) and self.is_empty_filter(search_arrival_value)):
            rights_ids = tuple({i.pk for i in self.user_branch_access})
            return self.custom_transport_select(rights_ids)

        self.filtered_by = f'&owner={search_owner_value}&from-location={search_from_value}&departure-date={search_departure_value}&arrival-date={search_arrival_value}'
        self.search_val = {
            'owner': search_owner_value,
            'from': search_from_value,
            'departure': search_departure_value,
            'arrival': search_arrival_value
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
        if not (re.match(pattern, input)):
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


    def custom_transport_select(self, access_list):
        queryset = Transportations.objects.none()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT 
                            tra.id, 
                            email,
                            u.id AS owner_id,
                            concat_ws(',', from_l.zip_code, from_l.city, from_l.country) AS from_id, 
                            concat_ws(',', to_l.zip_code, to_l.city, to_l.country) AS to_id, 
                            departure_time, 
                            arrival_time, 
                            ldm 
                    FROM transport_management_transportations AS tra
                    LEFT JOIN user_management_myuser AS u ON u.id = tra.owner_id_id	
                    LEFT JOIN known_locations_management_location AS from_l ON from_l.id = from_id_id
                    LEFT JOIN known_locations_management_location AS to_l ON to_l.id = to_id_id
                    WHERE u.branch_id in %s;
                """, [access_list])
            queryset = self.refactor_as_dictionary(cursor)
        return queryset


    def refactor_as_dictionary(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        
    

@method_decorator(decorators, name="dispatch")
class AddTransportationView(FormView):
    template_name = "transport_management/transportation_form.html"
    form_class = CreateTransportForm
    success_url = reverse_lazy('transportation-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Add Transport'
        context['form_action_type'] = 'Add'
        context['location_list'] = Location.objects.all()
        return context


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        form_fields = form.cleaned_data
        try:
            with transaction.atomic():
                
                from_location_id = get_or_create_location(str(form_fields['from_id']).strip())
                to_location_id = get_or_create_location(str(form_fields['to_id']).strip())

                Transportations.objects.create(
                    owner_id=self.request.user,
                    from_id=from_location_id,
                    to_id=to_location_id,
                    departure_time=form_fields['departure_time'],
                    arrival_time=form_fields['arrival_time'],
                    ldm=form_fields['ldm'],
                    weight=form_fields['weight'],
                    info=form_fields['info']
                )
        except IntegrityError as error_message:
            print(error_message)
        return HttpResponseRedirect(self.get_success_url())



@method_decorator(decorators, name="dispatch")
class UpdateTransportationView(FormView):
    template_name = "transport_management/transportation_form.html"
    form_class = UpdateTransportForm
    success_url = reverse_lazy('transportation-list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Transport'
        context['form_action_type'] = 'Update'
        context['location_list'] = Location.objects.all()
        return context


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()


        pk = self.kwargs['pk']
        try:
            transportation = Transportations.objects.get(id=pk)
        except Transportations.DoesNotExist:
            raise Http404

        if transportation.owner_id.pk != self.request.user.id:
            raise Http404

        kwargs = self.get_form_kwargs()
        kwargs['transportation'] = transportation

        return form_class(**kwargs)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        form_fields = form.cleaned_data
        pk = self.kwargs['pk']

        try:
            with transaction.atomic():
                from_location_id = get_or_create_location(str(form_fields['from_id']).strip())
                to_location_id = get_or_create_location(str(form_fields['to_id']).strip())

                Transportations.objects.filter(id=pk).update(
                    owner_id=self.request.user,
                    from_id=from_location_id,
                    to_id=to_location_id,
                    departure_time=form_fields['departure_time'],
                    arrival_time=form_fields['arrival_time'],
                    ldm=form_fields['ldm'],
                    weight=form_fields['weight'],
                    info=form_fields['info']
                )
        except IntegrityError as error_message:
            print(error_message)
        return HttpResponseRedirect(self.get_success_url())



class TransportationDetailView(DetailView):
    model = Transportations
    template_name = 'transport_management/transportation_detail.html'

    def get_queryset(self): 
        user_branch_access = {obj.object for obj in serializers.deserialize("json", self.request.session['logged_in_user_access'])}
        pk = self.kwargs['pk']
        transport = Transportations.objects.filter(Q(id=pk) & Q(owner_id__branch__in=user_branch_access))
        return transport



class TransportationDeleteView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'transportation-list'

    def get_redirect_url(self, *args, **kwargs):
        to_delete_ids = self.request.POST.getlist('data')
        logged_in_user = self.request.user

        try:
            with transaction.atomic():
                to_delete_transport_list = Transportations.objects.filter(Q(id__in=to_delete_ids) & Q(owner_id=logged_in_user.id))
                to_delete_transport_list.delete() 
        except IntegrityError as error_message:
            print(error_message)

        return super().get_redirect_url(*args, **kwargs)


def get_or_create_location(input):
    pattern = r'([0-9]{5,10})[ ,/.]([A-Z][a-z]{1,69})[ ,/.]([A-Z]{2,4})'
    from_location = re.match(pattern, input)

    try:
        from_location_id = Location.objects.get(zip_code=from_location.group(1),
                                                city=from_location.group(2),
                                                country=from_location.group(3)
                                                )
    except ObjectDoesNotExist:
        from_location_id = Location.objects.create(
            zip_code=from_location.group(1),
            city=from_location.group(2),
            country=from_location.group(3)
        )
        
    return from_location_id
