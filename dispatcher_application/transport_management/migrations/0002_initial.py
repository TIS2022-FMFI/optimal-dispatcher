# Generated by Django 4.1.3 on 2022-11-30 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transport_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transportations',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transportations',
            name='to_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_id', to='transport_management.location'),
        ),
    ]