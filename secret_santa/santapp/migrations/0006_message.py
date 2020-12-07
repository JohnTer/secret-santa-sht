# Generated by Django 3.1.4 on 2020-12-07 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santapp', '0005_auto_20201207_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('text', models.CharField(max_length=2048)),
                ('attachment_filename', models.CharField(max_length=64)),
            ],
        ),
    ]
