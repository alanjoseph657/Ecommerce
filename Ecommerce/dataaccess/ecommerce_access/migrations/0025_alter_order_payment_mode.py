# Generated by Django 5.0.7 on 2024-08-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_access', '0024_alter_cartreservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Card'), ('UPI', 'UPI'), ('BANK_TRANSFER', 'Bank Transfer')], default='CASH', max_length=20),
        ),
    ]
