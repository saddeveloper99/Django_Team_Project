from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Post


#게시글 작성
# @login_required
def create_post(request):
    user = request.session.get('user')
    context = {}
    #로그인한 사용자가 아니라면
    # if not user:
    #     return redirect('/')

    #HTML 출력
    if request.method == 'GET':
        return render(request,'tweet/create_post.html')

    # 데이터 수집
    elif request.method == 'POST':
        url = request.POST.get('url','')
        title = request.POST.get('title','')
        comment = request.POST.get('comment','')
        owner = request.user.id

        # 데이터 검사
        if not all([url,title,comment]):
            return render(request, 'tweet/create_post.html',context)

        # 게시글 저장
        # new_post = Post.objects.create(id=owner,url=url,title=title,comment=comment)

        # # 나의 게시글 목록 가져오기, 정렬은 수정 순서가 아닌 생성시간 기준
        # my_post = Post.objects.filter(id=owner).order_by('-create_at')
        # context.update(my_post)

        # 게시글 저장후, 마이페이지로 이동
        return render(request,'tweet/create_post.html')
        # return render(request,'마이페이지.html',{'context':context})

# 게시글 수정
# @login_required
def set_post(request,post_id):
    url = request.POST.get('url', '')
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')


    post = Post.objects.get(id=post_id)
    context = {}
    if request.method == 'GET':
        context['post'] = post
        return render(request,'tweet/set_post.html',context)
    elif request.method == 'POST':
        pass

# 게시글 삭제
# @login_required
def delete_post(request,post_id):
    if request.method == 'GET':
        return redirect('/')
    elif request.method =='POST':
        # 선택한 post_id의 id값을 읽어온다.
        try:
            owner = Post.objects.get(id = post_id)
        except:
            return redirect('/')

        # 현재 접근한 유저와, 소유자의  id와 같은지 판별하고 데이터를 삭제한다.
        if request.user.id == owner.id:
            owner.delete()
        else:
            return redirect('/')

        # 삭제하고난 다음, 소유자의 모든 post를 조회한다.
        post = Post.objects.filter(id=owner)
        # return render(request,'마이 페이지.html',post)
