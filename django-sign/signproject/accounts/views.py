from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            User.objects.create_user(request.POST['username'], password=request.POST['password1'])
        return redirect('index')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        # 입력받은 id와 pw가 데이터베이스에 있는지 확인
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        # 해당 데이터의 유저가 있으면 로그인하고 index로 redirect
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        # 없으면 에러 표시하고 login로 새로고침
        else:
            return render(request, 'login.html', {'error': '❗ username or password is incorrect. ❗'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def userpage(request):
    # 로그인 했을 경우 해당 페이지 접속
    if request.user.is_authenticated:
        return render(request, 'userpage.html')
    else:
        return render(request, 'index.html', {'userpage_error': 'Only site member can access this page'})