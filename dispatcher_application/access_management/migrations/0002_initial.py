# Generated by Django 4.1.3 on 2023-02-03 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access_management', '0001_initial'),
        ('branch_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroupaccess',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userbranchaccess',
            name='branch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_management.branch'),
        ),
        migrations.AddField(
            model_name='userbranchaccess',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupbranchaccess',
            name='branch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_management.branch'),
        ),
        migrations.AddField(
            model_name='groupbranchaccess',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='access_management.group'),
        ),
        migrations.AddConstraint(
            model_name='usergroupaccess',
            constraint=models.UniqueConstraint(fields=('group_id', 'user_id'), name='unique_group_access_record'),
        ),
        migrations.AddConstraint(
            model_name='userbranchaccess',
            constraint=models.UniqueConstraint(fields=('branch_id', 'user_id'), name='unique_branch_record'),
        ),
        migrations.AddConstraint(
            model_name='groupbranchaccess',
            constraint=models.UniqueConstraint(fields=('group_id', 'branch_id'), name='unique_group_record'),
        ),
    ]
