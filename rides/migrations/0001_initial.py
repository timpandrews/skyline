# Generated by Django 3.1 on 2020-10-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('duration', models.DurationField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('average_speed', models.DecimalField(decimal_places=2, max_digits=5)),
                ('calories', models.PositiveSmallIntegerField(blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
    ]