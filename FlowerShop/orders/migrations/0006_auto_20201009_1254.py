# Generated by Django 3.1.1 on 2020-10-09 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20201008_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address_detail',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
    ]