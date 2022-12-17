import datetime
from django.db import connections
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from datetime import datetime

class TransportationView(View):
    template = "transportation_form.html"

    def get(self, request):
        context = {}
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
        info = request.POST['notes']

        self.insert_transport(from_location, to_location, departure_date, departure_time, arrival_date, arrival_time,
                              ldm, weight, info)
        return redirect('/transports')

    def insert_transport(self, from_location, to_location, departure_date, departure_time, arrival_date, arrival_time,
                         ldm, weight, info):
        departure = datetime.combine(parse_date(departure_date), parse_time(departure_time))
        arrival = datetime.combine(parse_date(arrival_date), parse_time(arrival_time))

        # TODO toto prepisat na realnu databazu + user_id zistit ako doplnit
        cursor = connections['default'].cursor()
        cursor.execute(
            "INSERT INTO transportations(from_id, to_id, departure, arrival, ldm, weight, info)"
            "VALUES( %s, %s, %s, %s, %s, %s, %s)",
            [from_location, to_location, departure, arrival, ldm, weight, info])



