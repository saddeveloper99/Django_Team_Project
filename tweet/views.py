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
        owner = request.user

        # 데이터 검사
        if not all([url,title,comment]):
            return render(request, 'tweet/create_post.html',context)

        # 게시글 저장
        # new_post = Post.objects.create(id2=owner,url=url,title=title,comment=comment)

        # # 나의 게시글 목록 가져오기, 정렬은 수정 순서가 아닌 생성시간 기준
        # my_post = Post.objects.filter(id2=owner).order_by('-create_at')
        # context.update(my_post)

        # 게시글 저장후, 마이페이지로 이동
        return render(request,'tweet/create_post.html')
        # return render(request,'tweet/create_post.html',{'context':context})