from django.shortcuts import render

def create_post(request):
    return render(request,'tweet/create_post.html')