from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('introduce/', views.introduce, name="introduce"),
    path('profile/<int:designer_id>/', views.detail, name="detail"),

    # Create - 디자이너 등록하기
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),

    # Delete - 정보 삭제
    path('delete/<int:designer_id>/', views.delete, name="delete"),
]
