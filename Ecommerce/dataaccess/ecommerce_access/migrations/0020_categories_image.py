# Generated by Django 5.0.7 on 2024-08-12 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_access', '0019_verificationotp_email_alter_verificationotp_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/'),
        ),
    ]
