import os
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from django.utils import timezone

# Create your models here.

class MainPageContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    intro_text = models.TextField()

    def __str__(self):
        return self.title


class DropdownItem(models.Model):
    page = models.ForeignKey(MainPageContent, on_delete=models.CASCADE, related_name="dropdowns")
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
    

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # bullet points
    drive_link = models.URLField(max_length=500, blank=True)
    
    def __str__(self):
        return self.title
    
class Topic_title(models.Model):
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description[:50]  # returner en del av beskrivelsen
    

class PageVisit(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    referer = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} visited {self.path} at {self.created_at}"
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Trusted user feature
    is_trusted = models.BooleanField(default=False, help_text="Can add courses to the platform")
    trusted_since = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_profile_image(self):
        """Return profile image URL or default image"""
        if self.profile_image:
            return self.profile_image.url
        return '/static/home/images/user.png'  # default image path


# Automatically create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


