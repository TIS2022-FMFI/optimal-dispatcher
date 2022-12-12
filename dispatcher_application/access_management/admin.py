from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Groups)
admin.site.register(User_group_access)
admin.site.register(User_branch_access)

