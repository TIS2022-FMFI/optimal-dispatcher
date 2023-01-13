from django.test import SimpleTestCase
from django.urls import resolve,reverse
from authentication.views import *

class TestUrls(SimpleTestCase):
    def test_login_url(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func.view_class,LoginView)
    
    # def test_logout_url(self):
    #     url = reverse("logout")
    #     self.assertEquals(resolve(url).func.view_class,LogoutView)
        
