from django.test import SimpleTestCase
from django.urls import resolve,reverse
from access_management.views import *


class TestUrls(SimpleTestCase):
        
    def test_group_list_url(self):
        url = reverse("group-list")
        self.assertEquals(resolve(url).func.view_class,ListGroupsView)
    
    def test_group_add_url(self):
        url = reverse("group-add")
        self.assertEquals(resolve(url).func.view_class,CreateGroupView)
        
    def test_group_delete_url(self):
        url = reverse("group-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class,DeleteGroupView)
        


    def test_group_access_list_url(self):
        url = reverse("group-access", args=[1])
        self.assertEquals(resolve(url).func.view_class,GroupAccessView)
    
    def test_group_access_add_url(self):
        url = reverse("group-access-add", args=[1])
        self.assertEquals(resolve(url).func.view_class,AddGroupAccessView)
        