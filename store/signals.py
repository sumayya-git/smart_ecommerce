from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

from django.db.models.signals import post_delete
from django.core.cache import cache
from .models import Product, Category


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, **kwargs):
    cache.clear()
    print("Redis Cache Cleared (Product)")


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, **kwargs):
    cache.clear()
    print("Redis Cache Cleared (Category)")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)