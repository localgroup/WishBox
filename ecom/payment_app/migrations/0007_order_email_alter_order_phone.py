# Generated by Django 5.0.6 on 2024-08-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0006_remove_order_email_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
