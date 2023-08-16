from django.db import models
from register.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Create your models here.



class UserProfileModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=255, blank=True, null=True )
    last_name = models.CharField(max_length=255, blank=True, null=True )
    address = models.TextField( )
    created_at = models.DateTimeField(auto_now=True)
    state= models.CharField(max_length=255, blank=True, null=True)
    lga = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()