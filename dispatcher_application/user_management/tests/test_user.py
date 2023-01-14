from django.test import TestCase
from user_management.models import MyUser
from branch_management.models import Branch


class UserTestCase(TestCase):
    
    #not sure ci to nema byt v authentication ...
    
    def setUp(self):
        
        self.branch1 = Branch.objects.create(
            name = "Trnava"
        )
        
        user = MyUser(
            email="testik@gefco.net", 
            first_name = "Bala",
            last_name = "Lajka",
            password="password",
            branch = self.branch1
        )
        user.is_superuser = False
        user.save()
        
        admin_user = MyUser(
            email="testik_admin@gefco.net", 
            first_name = "Admin",
            last_name = "Lajka",
            password="password2",
            branch = self.branch1
        )
        user.is_superuser = True
        admin_user.save()
        
    def test_user_count(self):
        self.assertEqual(MyUser.objects.all().count(),2)
        
    def test_login_user(self):
        login_url = "/authentication/login/"
        data = {"email":"testik@gefco.net","password":"password"}
        response = self.client.post(login_url,data,follow=True)
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
        
    def test_login_superuser(self):
        login_url = "/authentication/login/"
        data = {"email":"testik_admin@gefco.net","password":"password2"}
        response = self.client.post(login_url,data,follow=True)
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
        
    def test_login_user_false(self):
        login_url = "/login/"
        data = {"email":"testik@gefco.net","password":"p"}
        response = self.client.post(login_url,data,follow=True)
        status_code = response.status_code
        self.assertEqual(status_code,404)