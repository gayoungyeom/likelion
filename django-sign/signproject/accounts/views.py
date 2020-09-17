from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], request.POST['password1'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST['email']
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            return render(request, 'index.html', {'check_error': 'Please check your account activation email'})
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'index.html', {'activate_account': 'Your Accounts is activate'})
    else:
        return render(request, 'index.html', {'activate_error': '계정 활성화 오류'})
    return