from django urls import path
from .views import ListTransactionView

urlpatterns = [
    path('transports/', ListTransactionView.as_view(), name = 'transport_list'),
]