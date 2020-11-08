from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Signalling showing above will define signals of the User and Profile model,
# Therefore the Profile model will be automatically created/updated when the updated/created User


class Tile(models.Model):
    STATUS = (
        ('LIVE', 'LIVE'),
        ('PENDING', 'PENDING'),
        ('ARCHIVED', 'ARCHIVED'),
    )

    tile_name = models.CharField(max_length=200, null=True)
    launch_date = models.DateField(null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.tile_name


class Task(models.Model):
    TYPE = (
        ('SURVEY', 'SURVEY'),
        ('DISCUSSION', 'DISCUSSION'),
        ('DIARY', 'DIARY'),
    )
    profile = models.ForeignKey(
        Profile, related_name="profile_user", on_delete=models.CASCADE)
    tile = models.ForeignKey(Tile, related_name="tile",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True)
    order_field = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True, choices=TYPE)

    def __str__(self):
        return self.title
