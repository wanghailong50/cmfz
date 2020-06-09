from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect
from indexapp.models import TUser
import random,string
from userapp.captcha.image import ImageCaptcha
# Create your views here.
import uuid,random


def register_page(request):
    return render(request,'register.html')


def register(request):
    phone=request.POST.get('user')
    flag=TUser.objects.filter(username=phone)
    if flag:
        return HttpResponse('0')
    else:
        return HttpResponse('1')


def getcaptcha(request):
    image=ImageCaptcha()
    code=random.sample(string.ascii_letters+string.digits,4)
    code=''.join(code)
    data=image.generate(code)
    request.session['code']=code
    return HttpResponse(data,'image/png')


# 验证验证码


def check_captcha(request):
    page_captcha=request.POST.get('captcha')
    code=request.session['code']
    print(code)
    if page_captcha==code:
        return HttpResponse('0')
    else:
        return HttpResponse('1')


def register_data(request):
    user=request.session.get('user')
    return render(request,'register ok.html',{'user':user})


def login_page(request):
    print(1111)
    url = request.GET.get('url')
    print(url,111111)
    request.session['url']=url
    return render(request,'login.html')


def login(request):
    user=request.POST.get('user')

    pwd=request.POST.get('pwd')
    print(user,pwd)
    rember=request.POST.get('rember')
    users=TUser.objects.filter(username=user,password=pwd)
    url = request.session.get('url')
    print(url,64646464,users)
    response = HttpResponse(url)
    if users:
        request.session["is_login"]=True
        request.session['user'] = user
        if rember=='true':
            response.set_cookie('user',user,max_age=7*24*3600)
            response.set_cookie('pwd',pwd,max_age=7*24*3600)
        return response
    return HttpResponse('1')


def test(request):
    url=request.GET.get('url')
    request.session["url"] = url
    return HttpResponse('1')


def mail(request):
    pwd = request.GET.get('pwd')
    user = request.GET.get('user')
    TUser.objects.create(username=user, password=pwd)

    request.session['user']=user
    return render(request,'mail.html',{'user':user})


def req(request):
    user=request.session.get('user')   #获取注册用户的账号
    list=''
    for i in range(4):
        result=random.randrange(0,4)
        list=list+str(result)
    request.session['list']=list
    from django.core.mail import send_mail
    send_mail('Subject here',list,'1412986060@qq.com',
              [user],fail_silently=False)


    return HttpResponse('1')


def code(request):
    code = request.GET.get('code')  # 获取前段用户输入的验证码
    list=request.session.get('list')
    print(code, 1)
    print(list, 1)
    if int(code)==int(list):
        return HttpResponse('1')
    return HttpResponse('0')