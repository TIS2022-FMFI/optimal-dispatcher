from django.test import SimpleTestCase
from django.urls import resolve,reverse
from user_settings.views import *

class TestUrls(SimpleTestCase):
    def test_user_settings_url(self):
        url = reverse("user-settings")
        self.assertEquals(resolve(url).func.view_class,UserSettingsView)
    
    def test_user_password_change_url(self):
        url = reverse("user-password-change")
        self.assertEquals(resolve(url).func.view_class,ChangePasswordView)
        