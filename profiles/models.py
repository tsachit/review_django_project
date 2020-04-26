import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def create_token():
    return uuid.uuid1()

def image_path(profile, filename):
    # file will be uploaded to MEDIA_ROOT/profiles/<token>/image/<filename>
    return 'profiles/{0}/image/{1}'.format(profile.token, filename)

def resume_path(profile, filename):
    # file will be uploaded to MEDIA_ROOT/profiles/<token>/resume/<filename>
    return 'profiles/{0}/resume/{1}'.format(profile.token, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    token = models.CharField(max_length=50, default=create_token, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=image_path,null=True, blank=True)
    resume = models.FileField(upload_to=resume_path,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()