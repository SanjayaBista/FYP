# Generated by Django 4.0.1 on 2022-04-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_refund'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundMsg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=100)),
                ('prodid', models.CharField(max_length=100)),
            ],
        ),
    ]
