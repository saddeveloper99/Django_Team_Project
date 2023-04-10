from django.db import models
# Create your models here.

class Post(models.Model):
    class Meta:
        db_table = 'post'
    #id2 = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    like_count = models.PositiveIntegerField()
