from django.db import models
from user_management.models import MyUser
from branch_management.models import Branch

class Group(models.Model):
    name = models.CharField(max_length=50,null=False,unique=True)
    
    def __str__(self):
        return f'{self.name}'


class GroupBranchAccess(models.Model):
    group_id = models.ForeignKey(Group,on_delete=models.CASCADE,null=False) 
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'branch_id'], name='unique_group_record'),
        ]

    def __str__(self):
        return f'{self.group_id}, {self.branch_id}'


class UserGroupAccess(models.Model):
    group_id = models.ForeignKey(Group,on_delete=models.CASCADE,null=False) 
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'user_id'], name='unique_group_access_record'),
        ]

    def __str__(self):
        return f'{self.group_id}, {self.user_id}'


class UserBranchAccess(models.Model):
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch_id', 'user_id'], name='unique_branch_record'),
        ]

    def __str__(self):
        return f'{self.branch_id}, {self.user_id}'
