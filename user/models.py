from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"
    user_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=256, blank=True)
    image = models.ImageField(null=True, upload_to="", blank=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')
    