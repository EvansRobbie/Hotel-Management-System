from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField

GENDER = (
    ("Male", "Male"), ("Female","Female"), ("Other","Other")

)
IDENTITY_TYPE = (
    ("National Identification Number", "National Identification Number"), ("Drivers License","Drivers License"), ("International Passport","International Passport")

)

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

class User(AbstractUser):
    full_name =  models.CharField(max_length=255, null=True, blank=True)
    username =  models.CharField(max_length=255, unique=True)
    email =  models.EmailField(max_length=255, unique=True)
    phone_number: str = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER, default="Other")

    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    pid = ShortUUIDField(length=8, max_length=25,primary_key=True, alphabet="abcdefghijklmnopqrst1234567890") 
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True, default="default.png")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name =  models.CharField(max_length=255, null=True, blank=True)
    phone_number: str = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)

    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, null=True, blank=True)
    identity_image = models.FileField(upload_to=user_directory_path, null=True, blank=True, default="id.png")

    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-create_at"]

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else: return f"{self.user.username}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
