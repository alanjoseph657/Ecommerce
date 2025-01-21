from django.db.models import Q
from django.utils import timezone

from Ecommerce.dataaccess.ecommerce_access.advertisement_models import Advertisements


class AdvertisementDA():

    def __init__(self):
        pass

    def get_advertisements(self):
        return Advertisements.objects.all()
    
    def get_active_advertisements(self):
        return Advertisements.objects.filter(is_active=True)
    
    def add_advertisements(self, data_dict):
        try:
            obj = Advertisements.objects.create(**data_dict)
        except Exception as err:
            return str(err)
        return obj
    
    def update_advertisements(self, offer_id, data_dict):
        try:
            updated = Advertisements.objects.filter(id = offer_id).update(**data_dict)
        except Exception as err:
            return str(err)
        return updated

    def get_offer_start_date(self, offer_id):
        return Advertisements.objects.filter(id=offer_id).values('start_date')
    
    def get_offer_end_date(self, offer_id):
        return Advertisements.objects.filter(id=offer_id).values('end_date')
    
    def get_offers_by_product(self, product_id):
        try:
            current_date = timezone.now()
            obj = Advertisements.objects.filter(
                Q(product_id=product_id) & 
                (Q(start_date__gte=current_date) | Q(is_active=True)))
        except Advertisements.DoesNotExist:
            return None
        return obj
    
    def get_valid_offers(self):
        try:
            current_date = timezone.now()
            obj = Advertisements.objects.filter(
                Q(start_date__gte=current_date) | Q(is_active=True))
        except Advertisements.DoesNotExist:
            return None
        return obj