# Generated by Django 5.0.7 on 2024-07-24 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartReservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('variant_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('RESERVED', 'Reserved'), ('EXPIRED', 'Expired')], default='RESERVED', max_length=10)),
                ('reserved_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField()),
                ('variant_id', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('reorder_level', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField()),
                ('variant_id', models.IntegerField()),
                ('change', models.IntegerField()),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', ' Pending'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=10)),
                ('payment_mode', models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Card'), ('UPI', 'UPI'), ('BANK_TRANSFER', 'Bank Transfer')], default='BANK_TRANSFER', max_length=20)),
                ('payment_status', models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('REPAYMENT_COMPLETED', 'Repayment Completed'), ('REPAYMENT_INITIATED', 'Repayment Initiated')], default='UNPAID', max_length=20)),
                ('reference_number', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_address_id', models.IntegerField()),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('variant_id', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('change_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('variant_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wishlist_id', models.IntegerField()),
                ('product_id', models.IntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
