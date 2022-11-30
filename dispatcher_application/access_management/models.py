from django.db import models
from user_management.models import MyUser
from branch_management.models import Branch

class Groups(models.Model):
    group_name = models.CharField(max_length=40,null=False)

    def __str__(self):
        return self.group_name


class Group_branch_access(models.Model):
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    write_access = models.BooleanField(default=False)


class User_group_access(models.Model):
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False) 
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 


class User_branch_access(models.Model):
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    write_access = models.BooleanField(default=False)
