from django.shortcuts import render,redirect

def comment_view(request):
    return render(request,'comment_test.html')

