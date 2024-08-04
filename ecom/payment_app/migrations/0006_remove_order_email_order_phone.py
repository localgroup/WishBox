# Generated by Django 5.0.6 on 2024-08-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0005_shippingaddress_shipping_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.EmailField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
