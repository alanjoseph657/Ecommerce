from django.db import models
    

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.FileField(upload_to='user_media/',blank=True, null=True) 


class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=100,blank=True, null=True)
    address_line1 = models.TextField()
    address_line2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    alt_number = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.IntegerField()
    is_default = models.BooleanField(default=False)
    used_for_last_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class ClientReport(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    report_name = models.CharField(max_length=255)
    report_data = models.TextField()
    created_by = models.IntegerField(null= True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report_name
    

class VerificationOtp(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    otp = models.IntegerField()


class ClientMessages(models.Model):
    OPEN = 'OPEN'
    REPLIED = 'REPLIED'
    CLOSED = 'CLOSED'
    status_choices = [
        (OPEN, 'Open'),
        (REPLIED, 'Replied'),
        (CLOSED, 'Closed'),
    ]
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default=OPEN)
    updated_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
