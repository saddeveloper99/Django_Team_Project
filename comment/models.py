from django.db import models
from tweet.models import Post
from user.models import UserModel

# Create your models here.

class PostCommentModel(models.Model):
    class Meta:
        db_table = 'comment'

    post_comment_id = models.AutoField(primary_key=True) #댓글번호
    post = models.ForeignKey(Post,on_delete=models.CASCADE) #포스트
    owner = models.ForeignKey(UserModel,on_delete=models.CASCADE)#user

    # 사용자는 여러개의 댓글을 작성할 수 있고, 포스트는 여러개의 댓글을 소유할 수 있다 ( one - to many)
    post_comment = models.TextField()
    com_created_at = models.DateTimeField(auto_now_add=True)
    com_updated_at = models.DateTimeField(auto_now=True)

    # like_history는 추후 적용을 강구해 본다.
    # like_count = models.PositiveIntegerField()