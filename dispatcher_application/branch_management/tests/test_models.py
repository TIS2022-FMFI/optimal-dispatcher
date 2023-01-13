from django.test import TestCase
from branch_management.models import Branch

class UserTests(TestCase):

    def setUp(self):
        self.b1 = Branch.objects.create(
            name = "branch1"
        )
        
        self.b2 = Branch.objects.create(
            name = "branch2"
        )
        
    
    def test_branch_count(self):
        self.assertEqual(Branch.objects.all().count(),2)
    
    
    def test_branch_equality(self):
        self.assertFalse(self.b1 == self.b2)
    
    
        