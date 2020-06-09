
from django.contrib import admin
from django.urls import path,include
from indexapp import views

app_name='indexapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('indexapp/',views.addemp,name='indexapp'),
    path('add/',views.add,name='add'),
    path('index',views.index,name='index'),
    path('details',views.details,name='details'),
    path('booklist',views.booklist,name='booklist'),
    path('login_out/',views.login_out,name='login_out'),
    path('listlogin_out/',views.listlogin_out,name='listlogin_out'),
    path('details_out',views.details_out,name='details_out'),
    path('addemp',views.addemp,name='addemp'),


]
