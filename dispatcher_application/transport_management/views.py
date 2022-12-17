from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
# Create your views here.
from .forms import *

# Create your views here.

def main(request):
    transports = Transportations.objects.all()
    
    show = True
    if transports.count() == 0:
        show = False
        
    context = {"transports":transports,"show":show}
    
    return render(request, "transport_management/transport_main.html", context)

def createTransport(request):
    form = TransportForm()
    if request.method == "POST":
        form = TransportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transport_data")
    
    context = {"form":form}
    return render(request, "transport_management/transport_add.html", context)

def updateTransport(request,pk):
    t = Transportations.objects.get(id=pk)
    form = TransportForm(instance=t)
    if request.method == "POST":
        form = TransportForm(request.POST,instance=t)
        if form.is_valid():
            form.save()
            return redirect("transport_data")
    
    show = False
    context = {"form":form,"show":show}
    return render(request, "transport_management/transport_add.html", context)


def deleteTransport(request):
    t = Transportations.objects.all()
    
    if request.method == "POST":
        pole = request.POST.getlist("data")
        print(pole)
        for i in pole:
            obj = Transportations.objects.get(id=i)
            obj.delete()
            
        return redirect("transport_data")
            
     
    context = {"transports":t}
    return render(request, "transport_management/transport_main.html", context)