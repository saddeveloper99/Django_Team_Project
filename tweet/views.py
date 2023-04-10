from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """
    메인페이지
    유저 정보 인증 후 경로 설정
    """

    return render(request, "tweet/home.html")


def create_post(request):
    return render(request, 'tweet/create_post.html')
