from django.db.models.signals import post_save
from django.dispatch import receiver
from register.models import CustomUser
from .models import UserProfileModel

@receiver(post_save, sender=CustomUser)
def ensure_user_profile(sender, instance, **kwargs):
    UserProfileModel.objects.get_or_create(user=instance)