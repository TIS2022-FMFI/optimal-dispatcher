from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('authentication/', include('authentication.urls')),
    path('admin-panel/user/', include('user_management.urls')),
    path('admin-panel/location/', include('known_locations_management.urls')),
    path('admin-panel/branch/', include('branch_management.urls')),
    path('admin-panel/access/', include('access_management.urls')),
]
