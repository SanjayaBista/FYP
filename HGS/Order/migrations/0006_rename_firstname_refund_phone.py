# Generated by Django 4.0.1 on 2022-04-12 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_refund'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refund',
            old_name='firstName',
            new_name='phone',
        ),
    ]