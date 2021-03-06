# Generated by Django 4.0.1 on 2022-04-27 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_alter_itemordered_order_alter_itemordered_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('reason', models.CharField(max_length=500)),
                ('refundOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Order.itemordered')),
            ],
        ),
    ]
