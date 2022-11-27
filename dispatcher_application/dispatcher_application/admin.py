from django.contrib import admin
from .models import *

admin.site.register(Location)
admin.site.register(Branch)
admin.site.register(Users)
admin.site.register(Groups)
admin.site.register(User_access)
admin.site.register(Group_access)
admin.site.register(Known_locations)
admin.site.register(Transportations)
