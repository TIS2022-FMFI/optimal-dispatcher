import datetime
from django.db import connections
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from datetime import datetime
from .models import Location
from django.core.exceptions import ObjectDoesNotExist


class TransportationView(View):
    template = "transportation_form.html"

    def get(self, request):
        location_list = Location.objects.all()
        context = {'location_list': location_list}
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

        error_message = ""

        from_id = self.get_location_id(from_location.split(","))
        to_id = self.get_location_id(to_location.split(","))

        if from_id == -1 or to_id == -1 or from_id == to_id:
            error_message = "Wrong location input"

        departure = datetime.combine(parse_date(departure_date), parse_time(departure_time))
        arrival = datetime.combine(parse_date(arrival_date), parse_time(arrival_time))

        if departure >= arrival:
            if error_message != "":
                error_message += '\n'
            error_message = "Departure cannot be later than arrival"

        if error_message != "":
            context = {'from_id': from_location, 'to_id': to_location, 'departure_date': departure_date,
                       'departure_time': departure_time, 'arrival_date': arrival_date, 'arrival_time': arrival_time,
                       'ldm': ldm, 'weight': weight, 'info': info, 'error_message': error_message}
            return render(request, self.template, context)


        self.insert_transport(from_id, to_id, departure, arrival, ldm, weight, info)
        # self.insert_transport(self.request.user.id, from_id, to_id, departure, arrival, ldm, weight, info)
        return redirect('/transports')

    def get_location_id(self, location):
        """
        returns id number of the location parameter
        if it doesn't already exist, creates a new location in the known_locations_management_location table
        """
        try:
            return Location.objects.get(zip_code=location[0], city=location[1], country=location[2]).id
        except IndexError:
            return -1
        except ObjectDoesNotExist:
            if len(location[0]) > 10 or len(location[1]) > 70 or len(location[2]) > 4:
                return -1

            new_location = Location()
            new_location.zip_code = location[0]
            new_location.city = location[1]
            new_location.country = location[2]
            new_location.save()
            return new_location.id


    def insert_transport(self, from_id, to_id, departure, arrival, ldm, weight, info):
        cursor = connections['default'].cursor()
        cursor.execute(
            "INSERT INTO transportations(from_id, to_id, departure, arrival, ldm, weight, info)"
            "VALUES( %s, %s, %s, %s, %s, %s, %s)",
            [from_id, to_id, departure, arrival, ldm, weight, info])


    # def insert_transport(self, user_id, from_id, to_id, departure, arrival, ldm, weight, info):
    #     cursor = connections['default'].cursor()
    #     cursor.execute(
    #         "INSERT INTO transport_management_transportations(owner_id_id,from_id_id,to_id_id,departure_time, arrival_time, ldm, weight, info)"
    #         "VALUES( %s, %s, %s, %s, %s, %s, %s, %s)",
    #         [user_id,from_id, to_id, departure, arrival, ldm, weight, info])
