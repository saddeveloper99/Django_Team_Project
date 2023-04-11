from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from .models import Post
from user.models import UserModel
from django.urls import reverse
def home(request):
    """
    메인페이지
    유저 정보 인증 후 경로 설정
    """

    return render(request, "tweet/home.html")

#게시글 작성
def create_post(request):
    #접근한 사용자가 로그인한 유저가 아니라면 로그인 페이지로 이동한다.
    user = request.user.is_authenticated
    if not user:
        return redirect(reverse('sign-in'))

    #HTML 출력
    if request.method == 'GET':
        return render(request,'tweet/create_post.html')

    # 데이터 수집
    elif request.method == 'POST':
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        comment = request.POST.get('comment','')
        owner = auth.get_user(request).user_id # son

        #접근한 유저가 UserModel에 등록된 사용자가 아닐경우 방지
        try :
            owner = UserModel.objects.get(user_id=owner) # 오브젝트 포링키에 있는지
        except UserModel.DoesNotExist:
            return redirect('/')

        # 데이터 검사
        if not all([url,title,comment]):
            return render(request, 'tweet/create_post.html',{'error':'빈칸 없이 입력해주세요.'})

        # 게시글 저장, # usermodeml 연결한 값 : user _id

        new_post = Post.objects.create(user_id=owner,url=url,title=title,comment=comment)
        # # 나의 게시글 목록 가져오기, 정렬은 수정 순서가 아닌 생성시간 기준
        my_post = Post.objects.filter(user_id=owner).order_by('-create_at')

        # 게시글 저장후, 상세페이지로 이동
        return render(request,'tweet/create_post.html')
        # return render(request,'상세페이지.html',{'my_post':my_post})

# 게시글 수정
def set_post(request,post_id):
    test = Post.objects.all()
    for i in test:
        print(i.post_id)

    print(post_id)

    #게시글이 없을 경우 방지
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')
    # 지급 현재 작업영역 계십니다.
    # 저장소에 최신 정보가 업데이트됬습니다.

    # 현재 브렌치에서 커밋하시고
    # 마스터로 체크아웃
    # 풀로 최신 정보 업데이트하시고
    # 브렌치랑 마스터 병합시고
    # 커밋하시고
    # 브렌치만들어서 작업

    print("통과!")
    #작성가 아닌 유저의 접근 방지
    user = auth.get_user(request)
    print(user.user_id) # 이름 user name
    print(post.user_id) # id
    print(post.user_id.user_id) # id
    if post.user_id !=  user.user_id:
        return redirect('/')
    print("두번째 통과!")
    # GET요청의경우, 이전에 작성해둔 post의 데이터와 함께 html을 출력한다.
    if request.method == 'GET':
        return render(request, 'tweet/set_post.html', {'post':post})

    # POST의경우 전달된 데이터를 토대로 게시글 수정
    elif request.method == 'POST':
        post.url = request.POST.get('url','')
        post.title = request.POST.get('title','')
        post.comment = request.POST.get('comment','')
        post.save()

        # 자신이 작성한 포스트의, 수정 순서가 아닌 최신 게시글 작성 순서로 정렬한다.
        post = Post.objects.filter(post_id=post_id).order_by('-create_at')
        return redirect('/')
        # return render(request, '상세페이지.html', {'post': post})

# 게시글 삭제
# @login_required
def delete_post(request,post_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method =='POST':

        # 선택한 post_id의 id값을 읽어온다.
        try:
            owner = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return redirect('/')

        # 현재 접근한 유저와, 소유자의  id와 같은지 판별하고 데이터를 삭제한다.
        if request.user.id == owner.id:
            owner.delete()
        else:
            return redirect('/')

        # 삭제하고난 다음, 소유자의 모든 post를 조회한다.
        post = Post.objects.filter(id=owner)
        # return render(request,'마이 페이지.html',post)
    return render(request, 'tweet/create_post.html')


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