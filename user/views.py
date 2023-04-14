from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model  # 사용자가 있는지 검사하는 함수
from django.contrib import auth  # 사용자 auth 기능
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import random

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인이 된 상태인지 확인
        if user:  # 로그인이 되어있다면
            return redirect('/')
        else:  # 로그인이 되어있지 않다면
            return render(request, 'user/signup.html')
    elif request.method == 'POST':  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        try:
            profile_image = request.FILES['profile-image']
        except:
            profile_image = None

        res_data = {}
        if password != password2:
            res_data['error'] = '비밀번호가 다릅니다. 다시 입력바랍니다.'
            return render(request, 'user/signup.html', res_data)
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                res_data['error'] = '이미 존재하는 아이디입니다.'
                return render(request, 'user/signup.html', res_data)  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            elif not all([username, password, password2]):
                res_data['error'] = '빈칸 없이 입력바랍니다.'
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'user/signup.html', res_data)
            elif username == '' or username.strip() == '':
                res_data['error'] = '아이디는 공백만으로 지을 수 없습니다.'
                return render(request, 'user/signup.html', res_data)
            else:
                new_user = UserModel.objects.create_user(
                    username=username, password=password)
                if profile_image:
                    # 프로필사진 파일에 랜덤성 부여!
                    profile_image.name = 'user' + str(new_user.user_id) + '_' + str(
                        random.randint(10000, 100000)) + '.' + str(profile_image.name.split('.')[-1])

                    # 파일 저장
                    file_system_storage = FileSystemStorage()
                    fs = file_system_storage.save(
                        profile_image.name, profile_image)

                    # 저장한 파일 url 따기
                    uploaded_file_url = file_system_storage.url(fs)

                    # 신규 회원의 user_id 따고 업데이트
                    check = UserModel.objects.filter(user_id=new_user.user_id)
                    check.update(image=uploaded_file_url)

                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username=username,
                               password=password)  # 사용자 불러오기
        res_data = {}
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')  # 로그인 성공 시 홈화면으로 가기
        else:  # 로그인 실패 시 로그인 페이지 보여주기
            res_data['error'] = '아이디 또는 비밀번호가 일치하지 않습니다.'
            return render(request, 'user/signin.html', res_data)
    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('/')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'user/signin.html')


@login_required
# 로그인 한 사용자만 접근 할 수 있게 하는 기능
# @login_required : 로그인 하지 않으면 접근 불가
# user = request.user.is_authenticated : 로그인의 여부만 검증 해 주는 기능
def logout(request):
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    return redirect("/")



# 팔로우 기능 구현

