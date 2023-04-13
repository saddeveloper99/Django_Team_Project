from django.db import models
from user.models import UserModel
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Post(models.Model):
    class Meta:
        db_table = 'post'
    owner = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    youtube_url = models.CharField(max_length=20)
    youtube_thumbnail = models.CharField(max_length=100)
    avg_star = models.FloatField(default=0, validators=[MinValueValidator(0,5),MaxValueValidator(5.0)])
