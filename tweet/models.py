from django.db import models
from user.models import UserModel
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
    avg_star = models.PositiveIntegerField(default=1)