from django.test import SimpleTestCase
from django.urls import resolve,reverse
from branch_management.views import *

class TestUrls(SimpleTestCase):
    def test_branch_list_url(self):
        url = reverse("branch-list")
        self.assertEquals(resolve(url).func.view_class,BranchListView)
    
    def test_branch_add_url(self):
        url = reverse("branch-add")
        self.assertEquals(resolve(url).func.view_class,AddBranchView)
        
    def test_branch_delete_url(self):
        url = reverse("branch-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class,DeleteBranchView)
        
    def test_branch_access_list_url(self):
        url = reverse("branch-access", args=[1])
        self.assertEquals(resolve(url).func.view_class,BranchAccessView)
    
    def test_branch_access_add_url(self):
        url = reverse("branch-access-add", args=[1])
        self.assertEquals(resolve(url).func.view_class,AddAccessView)
        