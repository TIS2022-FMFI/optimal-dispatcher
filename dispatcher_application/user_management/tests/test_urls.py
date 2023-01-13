from django.test import SimpleTestCase
from django.urls import resolve,reverse
from user_management.views import *

class TestUrls(SimpleTestCase):
    def test_user_list_url(self):
        url = reverse("user-list")
        self.assertEquals(resolve(url).func.view_class,ListAllUsersView)
    
    def test_user_add_url(self):
        url = reverse("user-add")
        self.assertEquals(resolve(url).func.view_class,RegisterNewUserView)
        
    def test_user_delete_url(self):
        url = reverse("user-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class,DeleteUserView)
        