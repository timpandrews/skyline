# Generated by Django 3.1 on 2020-12-02 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bike_name',
            field=models.CharField(default='bike_name', max_length=10),
            preserve_default=False,
        ),
    ]
