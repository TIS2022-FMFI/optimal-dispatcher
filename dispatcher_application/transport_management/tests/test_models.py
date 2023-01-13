from django.test import TestCase
from transport_management.models import Transportations
from user_management.models import *
from branch_management.models import Branch
from known_locations_management.models import Location
from datetime import datetime


class UserTests(TestCase):

    def setUp(self):
        datetime_str = '09/19/22 13:55:26'
        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        datetime_str2 = '09/20/22 15:55:26'
        datetime_object2 = datetime.strptime(datetime_str2, '%m/%d/%y %H:%M:%S')
        
        self.d1 = datetime_object
        self.d2 = datetime_object2
        
        self.branch1 = Branch.objects.create(
            name = "Trnava"
        )
        
        self.user = MyUser.objects.create(
            email="test.account@gefco.net", 
            first_name = "John",
            last_name = "Snow",
            branch = self.branch1
        )
        #self.user.branch = self.branch1
        #self.user.save()
        
        self.location = Location.objects.create(
            zip_code = "92401",
            city = "Galanta",
            country = "SK"
        )
        
        self.location2 = Location.objects.create(
            zip_code = "92601",
            city = "Sered",
            country = "SK"
        )
        
        self.t1 = Transportations.objects.create(
            owner_id = self.user,
            to_id = self.location,
            from_id = self.location2,
            departure_time = self.d1,
            arrival_time = self.d2,
            ldm = 8,
            weight = 100
        )
    
    
    def test_transportation_no_info(self):
        self.assertEqual(Transportations.objects.all().count(),1)
        

    def test_tranportation_add_info(self):
        self.t1.info = "some info"
        self.t1.save()
        
        self.assertEqual(str(self.t1.info),"some info")
        self.assertEqual(Transportations.objects.all().count(),1)
        
    
    def test_transportation_edit_data(self):
        t2 = Transportations.objects.create(
            owner_id = self.user,
            to_id = self.location2,
            from_id = self.location,
            departure_time = self.d2,
            arrival_time = self.d1,
            ldm = 6,
            weight = 50
        )
        t2.ldm = 8
        t2.save()
        
        self.assertEqual(str(t2.ldm),"8")
        self.assertEqual(Transportations.objects.all().count(),2)