from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('authentication.urls')),
    path('admin-panel/', include('user_management.urls')),
    path('admin-panel/', include('known_locations_management.urls')),
    path('admin-panel/', include('branch_management.urls')),
    path('admin-management/groups/', include('access_management.urls'))
]
