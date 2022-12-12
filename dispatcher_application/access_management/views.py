from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
# Create your views here.
from .forms import *

def main(request):
    groups = Groups.objects.all()
    
    context = {"groups":groups}
    
    return render(request, "access_management/group_main.html", context)

def createGroup(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("groups")
    
    context = {"form":form}
    return render(request, "access_management/group_add.html", context)

def updateGroup(request,pk):
    group = Groups.objects.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST,instance=group)
        if form.is_valid():
            form.save()
            return redirect("groups")
    
    context = {"form":form}
    return render(request, "access_management/group_add.html", context)


def deleteGroup(request):
    groups = Groups.objects.all()
    
    if request.method == "POST":
        pole = request.POST.getlist("data")
        print(pole)
        for i in pole:
            obj = Groups.objects.get(id=i)
            obj.delete()
            
        return redirect("groups")
            
     
    context = {"groups":groups}
    return render(request, "access_management/group_main.html", context)