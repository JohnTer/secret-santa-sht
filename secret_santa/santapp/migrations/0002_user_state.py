# Generated by Django 3.1.3 on 2020-11-28 19:18

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('santapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=django_fsm.FSMField(default='tutorial', max_length=50),
        ),
    ]
