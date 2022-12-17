import datetime
from django.db import connections
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from datetime import datetime
from .models import Location


class TransportationView(View):
    template = "transportation_form.html"

    def get(self, request):
        location_list = Location.objects.all()
        context = {'location_list': location_list}
        return render(request, self.template, context)

    def post(self, request):
        from_location = request.POST['from_id'].split(",")
        to_location = request.POST['to_id'].split(",")
        departure_date = request.POST['departure_date']
        departure_time = request.POST['departure_time']
        arrival_date = request.POST['arrival_date']
        arrival_time = request.POST['arrival_time']
        ldm = request.POST['ldm']
        weight = request.POST['weight']
        info = request.POST['notes']

        from_id = Location.objects.get(zip_code=from_location[0], city=from_location[1], country=from_location[2]).id
        to_id = Location.objects.get(zip_code=to_location[0], city=to_location[1], country=to_location[2]).id

        departure = datetime.combine(parse_date(departure_date), parse_time(departure_time))
        arrival = datetime.combine(parse_date(arrival_date), parse_time(arrival_time))

        self.insert_transport(from_id, to_id, departure, arrival, ldm, weight, info)

        return redirect('/transports')

    def insert_transport(self, from_id, to_id, departure, arrival, ldm, weight, info):
        cursor = connections['default'].cursor()
        cursor.execute(
            "INSERT INTO transportations(from_id, to_id, departure, arrival, ldm, weight, info)"
            "VALUES( %s, %s, %s, %s, %s, %s, %s)",
            [from_id, to_id, departure, arrival, ldm, weight, info])

        # cursor.execute(
        #     "INSERT INTO transport_management_transportations(owner_id_id,from_id_id,to_id_id,departure, arrival, ldm, weight, info)"
        #     "VALUES( %s, %s, %s, %s, %s, %s, %s, %s)",
        #     [owner_id,from_id, to_id, departure, arrival, ldm, weight, info])
