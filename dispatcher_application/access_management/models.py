from django.db import models
from user_management.models import MyUser
from branch_management.models import Branch

class Groups(models.Model):
    group_name = models.CharField(max_length=40,null=False)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return f'{self.group_name}, {self.branch_id}'


class User_group_access(models.Model):
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False) 
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'user_id'], name='unique_group_record'),
        ]


class User_branch_access(models.Model):
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False) 
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'branch_id'], name='unique_branch_record'),
        ]
