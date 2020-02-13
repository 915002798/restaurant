from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.


# 登录
from qiantai.models import Food


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)  # 根据获取的用户名密码去数据库查询，并返回user对象
    if request.POST:
        if user is not None and user.is_active:  # user不为空,并且仍在活跃
            auth.login(request, user)
            return redirect("/")  # 登陆成功，重定向到根路由
        else:
            return render(request, 'login/login.html')
    else:
        return render(request, 'login/login.html')


# 登出
def logout(request):
    auth.logout(request)  # 从请求中删除经过身份验证的用户的ID并刷新其会话数据。
    return redirect('/login/')


# 首页
@login_required(login_url='/login/')  # 登陆装饰器，指定本系统登录的 url
def index(request):
    foods = Food.objects.all()
    return render(request, 'login/index.html', {'user': request.user, 'foods': foods})
