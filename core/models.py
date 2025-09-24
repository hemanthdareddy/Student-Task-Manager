from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    CATEGORY_CHOICES = [
        ('consistency', 'Consistency'),
        ('workload', 'Workload'),
        ('special', 'Special Event'),
    ]
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon identifier - e.g., 🗓️")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_tier_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Ensure your User model automatically gets a profile when created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
       
class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Change the subject field from CharField to a ForeignKey
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title