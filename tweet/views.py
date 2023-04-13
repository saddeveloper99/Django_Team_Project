from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from .models import Post
from user.models import UserModel
from django.urls import reverse
from tweet.models import Post
from comment.models import PostCommentModel
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import random


def home(request):
    user = request.user.is_authenticated
    if user:
        all_post = Post.objects.all().order_by('-create_at')
        page = request.GET.get('page')
        paginator = Paginator(all_post, 8)
        page_obj = paginator.get_page(page)
        
        try:
            page_obj = paginator.page(page)
        except:
            page = 1
            page_obj = paginator.page(page)
        
        return render(request, 'tweet/home.html', {'all_post': all_post, 'page_obj' : page_obj})
    else:
        return redirect('/sign-in')

# 게시글 작성 ,login_required를 사용하는대신, 사용자를 로그인 페이지로 이동시킨다.
def create_post(request):
    # 접근한 사용자가 로그인한 유저가 아니라면 로그인 페이지로 이동한다.
    user = request.user.is_authenticated
    if not user:
        return redirect(reverse('sign-in'))
    # GET : 글 작성 페이지 이동

    if request.method == 'GET':
        return render(request, 'tweet/create_post.html')

    # 데이터 수집 및 저장
    elif request.method == 'POST':
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')
        owner = auth.get_user(request).user_id
        youtube_url = request.POST.get('youtube_url', '')
        #접근한 유저가 UserModel에 등록된 사용자가 아닐경우 방지
        try :
            owner = UserModel.objects.get(user_id=owner)
        except UserModel.DoesNotExist:
            return redirect('/')

        # youtube url 데이터 검사
        if 'youtube.com' in youtube_url :
            youtube_url_check = youtube_url.split('watch?v=')[1][:11]
        elif 'youtu.be' in youtube_url :
            youtube_url_check = youtube_url.split('be/')[1]
        else :
            return render(request, 'tweet/create_post.html', {'error': '유튜브 주소창을 입력해주세요.'})

        # 데이터 검사
        if not all([title, comment]):
            return render(request, 'tweet/create_post.html', {'error': '빈칸 없이 입력해주세요.'})
        # 게시글 저장,
        new_post = Post.objects.create(owner=owner,title=title,comment=comment,youtube_url=youtube_url_check)
        post_id = new_post.post_id
        # 게시글 저장후, 상세페이지로 이동
        return redirect(reverse('post-detail',args=[post_id]))

# 게시글 수정
def set_post(request,post_id):
    # 탐색하는 게시글이 없을 경우 방지
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')
    # 작성자와,접근자 아이디가 불일치 할경우
    user = auth.get_user(request)
    if post.owner.user_id != user.user_id:
        return redirect('/')

    # GET일경우 기존 작성된 내용을 참고하여 데이터 출력
    if request.method == 'GET':
        return render(request, 'tweet/set_post.html', {'post': post})

    # POST의경우 전달된 데이터를 토대로 게시글 수정
    elif request.method == 'POST':
        post.title = request.POST.get('title', '')
        post.comment = request.POST.get('comment', '')
        post.youtube_url = request.POST.get('youtube_url','')
        post.save()
        # 수정된 상세 페이지로 이동
        return redirect(reverse('post-detail',args=[post_id]))


# 게시글 삭제
def delete_post(request, post_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        # 선택한 post_id의 id값을 읽어온다, 이미 삭제됬을 경우를 방지하여 try except를 사용한다.
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return redirect('/')

        # 현재 접근한 유저와, 소유자의  id와 같은지 판별하고 데이터를 삭제한다.
        user = auth.get_user(request)
        if user.user_id != post.owner.user_id:
            post.delete()

        # 삭제후 마이페이지로 이동
        return redirect(reverse('set-profile',args=[post.owner.user_id]))


def my_page(request, user_id):
    # get일때, 유저 정보와 게시글들을 불러옴
    if request.method == "GET":
        # id로 선택한 유저의 정보를 가져옴
        click_user = UserModel.objects.get(user_id=user_id)
        # 유저 id가 post의 owner(fk)인 post를 가져와서
        # 사용자 user(me), 프로필 주인(click_user)가 같을때만 수정버튼 html에 
        me = request.user

        post = Post.objects.filter(owner=click_user).order_by('create_at')
        context = {
            'click_user': click_user,
            'posts': post,
            'me' : me,
        }
        return render(request, 'tweet/my_page.html', context)


def set_profile(request,user_id):
    # 메소드가 post일때, 유저네임, 프로필 사진, 프로필 메시지를 폼으로 받아온다.
    # 그리고 갱신하고 저장.
    if request.method == "POST":
        user = UserModel.objects.get(pk=user_id)
        me = request.user
        
        try:
            profile_image = request.FILES['profile-image']
            profile_image.name = 'user' + str(user.user_id) + '_' + str(random.randint(10000,100000)) + '.' + str(profile_image.name.split('.')[-1])
                    
            # 파일 저장
            file_system_storage = FileSystemStorage()
            fs = file_system_storage.save(profile_image.name, profile_image)
            
            # 저장한 파일 url 따기
            uploaded_file_url = file_system_storage.url(fs)
            
            user.image = uploaded_file_url
        except:
            pass

        new_username = request.POST.get('username', '')
        
        if get_user_model().objects.filter(username=new_username).exists() and new_username != user.username: 
            return render(request, 'tweet/set_profile.html', {'user': user, 'error':'이미 존재하는 사용자명입니다.'})
        elif new_username == '':
            return render(request, 'tweet/set_profile.html', {'user': user, 'error':'수정할 이름을 입력해주세요.'})
        else:
            user.username = new_username
            user.description = request.POST.get('description', '')
            user.save()
            post = Post.objects.filter(owner=user).order_by('create_at')
            context = {
                'click_user': user,
                'posts': post,
                'me': me,
            }
            return render(request, 'tweet/my_page.html', context)

    # get일때는, 유저 정보를 id로 받아와서, 수정창에 입력 돼 있게 하기.
    elif request.method == "GET":
        user = UserModel.objects.get(user_id=request.user.user_id)
        print(user.description)
        return render(request, 'tweet/set_profile.html', {'user': user})

def post_detail(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return redirect('/')

        post_comments = PostCommentModel.objects.filter(post_id=post_id)
        context = {'post':post,'post_comments':post_comments}

        return render(request, 'tweet/post_detail.html',context) #post_id를 받아와서 게시글 클릭하면 상세페이지로
        # 테스트 주석


