from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from .models import Post

def home(request):
    """
    메인페이지
    유저 정보 인증 후 경로 설정
    """

    return render(request, "tweet/home.html")

#게시글 작성
# @login_required
def create_post(request):
    # user = auth.get_user(request)
    # if user:
    #     return redirect('sign-in/')

    #HTML 출력
    if request.method == 'GET':
        return render(request,'tweet/create_post.html')

    # 데이터 수집
    elif request.method == 'POST':
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        comment = request.POST.get('comment','')
        owner = auth.get_user(request).id2
        # owner = UserModel.objects.get(id=owner)


        # 데이터 검사
        if not all([url,title,comment]):
            return render(request, 'tweet/create_post.html',{'error':'빈칸 없이 입력해주세요.'})

        # 게시글 저장
        # new_post = Post.objects.create(id=owner,url=url,title=title,comment=comment)

        # # 나의 게시글 목록 가져오기, 정렬은 수정 순서가 아닌 생성시간 기준
        # my_post = Post.objects.filter(id=owner).order_by('-create_at')
        # context.update(my_post)

        # 게시글 저장후, 상세페이지로 이동
        return render(request,'tweet/create_post.html')
        # return render(request,'상세페이지.html',{'context':context})

# 게시글 수정
# @login_required
def set_post(request,post_id):
    #게시글이 없을 경우 방지
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return redirect('/')


    context = {}
    if request.method == 'GET':
        context['post'] = post
        return render(request, 'tweet/set_post.html', context)
    elif request.method == 'POST':
        post.url = request.POST.get('url','')
        post.title = request.POST.get('title','')
        post.comment = request.POST.get('comment','')
        post.save()

        post = Post.objects.filter(post_id=post_id)
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
