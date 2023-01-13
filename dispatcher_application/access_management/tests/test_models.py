from django.test import TestCase
from access_management.models import *
from branch_management.models import Branch

class UserTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.g1 = Group.objects.create(
            name="group1"
        )

        self.g2 = Group.objects.create(
            name="group2"
        )
        
        self.b1 = Branch.objects.create(
            name = "branch1"
        )
        
        #print(self.g2.name)
        
    def test_group_creation(self):
        self.assertEqual(Group.objects.all().count(),2)
    
    
    def test_group_branch_access_creation(self):
        gb = GroupBranchAccess.objects.create(
            group_id = self.g1,
            branch_id = self.b1
        )
        
        self.assertEqual(GroupBranchAccess.objects.all().count(),1)
        self.assertEqual(gb.group_id, self.g1)
        
        gb.group_id = self.g2
        gb.save()
        
        self.assertEqual(GroupBranchAccess.objects.all().count(),1)
        self.assertEqual(gb.group_id, self.g2)