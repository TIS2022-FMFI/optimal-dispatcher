from django.test import SimpleTestCase
from django.urls import resolve,reverse
from transport_management.views import *

class TestUrls(SimpleTestCase):
    def test_transportation_list_url(self):
        url = reverse("transportation-list")
        self.assertEquals(resolve(url).func.view_class,ListTransportationsView)
    
    def test_transportation_add_url(self):
        url = reverse("transportation-add")
        self.assertEquals(resolve(url).func.view_class, AddTransportationView)
        
    