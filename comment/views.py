from django.shortcuts import render,redirect
from django.contrib import auth
from .models import PostCommentModel
from user.models import UserModel
from tweet.models import Post
from django.urls import reverse

def comment_view(request,post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')

    post_comments = PostCommentModel.objects.filter(post_id=post_id).order_by('-com_created_at')
    context ={'post':post,'post_comments':post_comments,}

    if request.method =='GET':
        # 해당 포스트에 관한 모든 댓글 내역을 조회한다.
        return render(request,'comment_test.html',context)

    elif request.method == 'POST':
        # 로그인 하지 않은 사용자는 로그인 페이지로 이동한다.
        user = request.user.is_authenticated
        if not user:
            return redirect(reverse('sign-in'))

        # 작성자 정보 가져오기
        try :
            owner = UserModel.objects.get(user_id= auth.get_user(request).user_id)
        except UserModel.DoesNotExist:
            return redirect('/')

        post_comment = request.POST.get('post-comment')
        new_post_commnet = PostCommentModel.objects.create(post=post,owner=owner,post_comment=post_comment,)

        return render(request,'comment_test.html',context)

############################################################################################################

def delete_comment(request,post_comment_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method =='POST':
        if not request.user.is_authenticated:
            return (reverse('sign-in'))
        user = auth.get_user(request)

        # try:
        #     comment_owner = PostCommentModel.objects.get(post_comment_id=post_comment_id)
        # except PostCommentModel.DoesNotExist:
        #     return redirect('/')
        #
        # if user.user_id != comment_owner.owner.user_id:
        #     return redirect('/')




