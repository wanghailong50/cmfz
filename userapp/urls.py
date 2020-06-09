
from django.contrib import admin
from django.urls import path,include
from indexapp import views
from userapp import views

app_name='userapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_page/',views.register_page,name='register_page'),
    path('register/',views.register,name='register'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('check_captcha/',views.check_captcha,name='check_captcha'),
    path('register_data/',views.register_data,name='register_data'),
    path('login_page',views.login_page,name='login_page'),
    path('login',views.login,name='login'),
    path('test',views.test,name='test'),
    path('mail',views.mail,name='mail'),
    path('req',views.req,name='req'),
    path('code',views.code,name='code'),
]
