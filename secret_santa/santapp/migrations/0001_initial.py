# Generated by Django 3.1.3 on 2020-11-28 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vk_id', models.IntegerField(unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('data_available_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=256)),
                ('wishlist', models.CharField(max_length=1024)),
                ('present_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='santapp.user')),
            ],
        ),
    ]