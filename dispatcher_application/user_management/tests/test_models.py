from django.test import TestCase
from user_management.models import MyUser

class UserTests(TestCase):

    @classmethod
    def setUpTestData(self):
        MyUser.objects.create(
            email="test.account@gefco.net", 
            first_name = "John",
            last_name = "Snow",
            password="password",
        )

        MyUser.objects.create(
            email="test.superuser@gefco.net", 
            first_name = "Admin",
            last_name = "Admin",
            password="admin",
            is_superuser = True
        )


    def testCreationOfRegularUser(self):
        user = MyUser.objects.get(email="test.account@gefco.net")
        self.assertEqual(user.email, "test.account@gefco.net")
        self.assertEqual(user.first_name, "John")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)


    def testCreationOfSuperUser(self):
        user = MyUser.objects.get(email="test.superuser@gefco.net")
        self.assertEqual(user.email, "test.superuser@gefco.net")
        self.assertNotEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    