from django.db import models


class Advertisements(models.Model):
    MAINPANEL = 'MAINPANEL'
    SUBPANEL = 'SUBPANEL'
    TYPE_CHOICES = [
        (MAINPANEL, 'Main Panel'),
        (SUBPANEL, 'Sub Panel')
    ]
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SUBPANEL)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='advertisements/',blank=True, null=True) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title