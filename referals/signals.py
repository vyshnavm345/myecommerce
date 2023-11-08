from .models import ReferenceProfile
from products.models import Custom_User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Custom_User)
def post_save_created_profile(sender, instance, created, *args, **kwargs):
    if created:
        ReferenceProfile.objects.create(user= instance)
