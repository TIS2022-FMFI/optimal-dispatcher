from django.test import SimpleTestCase
from django.urls import resolve,reverse
from known_locations_management.views import *

class TestUrls(SimpleTestCase):
    def test_location_list_url(self):
        url = reverse("location-list")
        self.assertEquals(resolve(url).func.view_class,ListLocatiosView)
    
    def test_location_add_url(self):
        url = reverse("location-add")
        self.assertEquals(resolve(url).func.view_class,AddLocationView)
        
    def test_location_delete_url(self):
        url = reverse("location-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class,DeleteLocationView)
        