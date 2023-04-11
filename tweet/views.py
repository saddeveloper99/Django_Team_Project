from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from .models import Post
from user.models import UserModel
from django.urls import reverse
def home(request):
    user = request.user.is_authenticated
    if user:
        return render(request, 'tweet/home.html')
    else:
        return redirect('/sign-in')

#게시글 작성 ,login_required를 사용하는대신, 사용자를 로그인 페이지로 이동시킨다.
def create_post(request):
    #접근한 사용자가 로그인한 유저가 아니라면 로그인 페이지로 이동한다.
    user = request.user.is_authenticated
    if not user:
        return redirect(reverse('sign-in'))
    # GET : 글 작성 페이지 이동
    if request.method == 'GET':
        return render(request,'tweet/create_post.html')

    # 데이터 수집 및 저장
    elif request.method == 'POST':
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        comment = request.POST.get('comment','')
        owner = auth.get_user(request).user_id
## 해치우자 !
        #접근한 유저가 UserModel에 등록된 사용자가 아닐경우 방지
        try :
            owner = UserModel.objects.get(user_id=owner)
        except UserModel.DoesNotExist:
            return redirect('/')

        # 데이터 검사
        if not all([url,title,comment]):
            return render(request, 'tweet/create_post.html',{'error':'빈칸 없이 입력해주세요.'})

        # 게시글 저장,
        new_post = Post.objects.create(owner=owner,url=url,title=title,comment=comment)

        # 게시글 저장후, 상세페이지로 이동
        return render(request,'tweet/create_post.html')
        # return redirect(reverse('상세페이지'))

# 게시글 수정
def set_post(request,post_id):
    #게시글이 없을 경우 방지
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')

    #작성가 아닌 유저의 접근 방지
    user = auth.get_user(request)
    if post.owner.user_id !=  user.user_id:
        return redirect('/')

    # GET요청의경우, 이전에 작성해둔 post의 데이터와 함께 html을 출력한다.
    if request.method == 'GET':
        return render(request, 'tweet/set_post.html', {'post':post})

    # POST의경우 전달된 데이터를 토대로 게시글 수정
    elif request.method == 'POST':
        post.url = request.POST.get('url','')
        post.title = request.POST.get('title','')
        post.comment = request.POST.get('comment','')
        post.save()

        return render(request, 'tweet/set_post.html', {'post':post})
        # return redirect(reverse('상세페이지'))

# 게시글 삭제
# @login_required() 현재 유저와, owner의 id값을 비교하는 분기문이 있으므로 사용할 필요가 없으리라 기대한다.
def delete_post(request,post_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method =='POST':
        # 선택한 post_id의 id값을 읽어온다, 이미 삭제됬을 경우를 방지하여 try except를 사용한다.
        try:
            post = Post.objects.get(post_id = post_id)
        except Post.DoesNotExist:
            return redirect('/')

        # 현재 접근한 유저와, 소유자의  id와 같은지 판별하고 데이터를 삭제한다.
        user = auth.get_user(request)
        if user.user_id != post.owner.user_id:
            post.delete()

        return redirect('/')
        # return redirect(reverse('상세페이지'))


def my_page(request, user_id):
    # get일때, 유저 정보와 게시글들을 불러옴
    if request.method == "GET":
        me = request.user
        # id로 선택한 유저의 정보를 가져옴
        click_user = UserModel.objects.get(id=user_id)
        # 유저 id가 post의 id2(fk)인 post를 가져와서 
        post = Post.objects.filter(id2=click_user).order_by('create_at')
        return render(request, 'tweet/my_page.html', {'click_user': click_user, 'post': post})

def edit_profile(request):
    if request.method == "POST":
        user = UserModel.objects.get(id=id)

        if request.user.id == user:
            
            # 폼데이터로 갱신
            user.save()
            
    elif request.method == "GET":
        user = UserModel.objects.get(id=request.user.id)
        return render(request, {'user': user})
    
def post_detail(request, user_id):
    return render(request, 'tweet/post_detail.html')