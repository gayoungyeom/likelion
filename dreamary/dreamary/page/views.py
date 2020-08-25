from django.shortcuts import render, get_object_or_404, redirect
from .models import Designer
# Create your views here.


def home(request):
    designers = Designer.objects.all()
    return render(request, 'home.html', {'designers': designers})


def introduce(request):
    return render(request, 'introduce.html')


def detail(request, designer_id):
    designer = get_object_or_404(Designer, pk=designer_id)
    return render(request, 'detail.html', {'designer': designer})


def new(request):  # 등록하기 버튼 누르면 new.html로 이동 (form)
    return render(request, 'new.html')


def create(request):  # 폼 작성 후 등록버튼 누르면 디자이너 등록 (action)
    if request.method == 'POST':  # method가 POST일 경우만 객체 생성
        post = Designer()
        if 'image' in request.FILES:  # 이미지가 실제로 들어온 경우만 이미지 등록
            post.image = request.FILES['image']  # [' ']안에 값은 html에서 설정한 name
        post.name = request.POST['name']
        post.address = request.POST['address']
        post.description = request.POST['description']

        post.save()
        return redirect('detail', post.id)


def delete(request, designer_id):  # detail 페이지의 정보 삭제 버튼 누르면 삭제
    post = get_object_or_404(Designer, pk=designer_id)
    post.delete()

    return redirect('home')


def update(request, designer_id):  # create과 달리 페이지 이동(GET)과 정보 수정(POST)을 한 메소드에서 진행
    post = get_object_or_404(Designer, pk=designer_id)

    if request.method == 'POST':
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.name = request.POST['name']
        post.address = request.POST['address']
        post.description = request.POST['description']

        post.save()
        return redirect('detail', post.id)

    else:  # reqeust == 'GET'
        return render(request, 'update.html', {'designer': post})
