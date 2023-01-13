from django.test import TestCase
from known_locations_management.models import Location

class UserTests(TestCase):

    def setUp(self):
        self.loc1 = Location.objects.create(
            zip_code = "92401",
            city = "Galanta",
            country = "SK"
        )
        
        self.loc2 = Location.objects.create(
            zip_code = "92601",
            city = "Sered",
            country = "SK"
        )
        
    
    def test_locations_count(self):
        self.assertEqual(Location.objects.all().count(),2)
        
    
    def test_locations_edit(self):
        self.loc1.zip_code = "92301"
        self.loc1.save()
        self.assertEqual(str(self.loc1.zip_code),"92301")
        self.assertEqual(Location.objects.all().count(),2)