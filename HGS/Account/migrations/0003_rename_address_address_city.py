# Generated by Django 4.0.1 on 2022-04-08 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_alter_address_postal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address',
            new_name='city',
        ),
    ]