# Generated by Django 4.1.3 on 2022-12-18 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('known_locations_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transportations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('ldm', models.FloatField()),
                ('weight', models.FloatField()),
                ('info', models.TextField(null=True)),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_id', to='known_locations_management.location')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_id', to='known_locations_management.location')),
            ],
        ),
    ]
