
from django.contrib import admin
from django.urls import path,include
from indexapp import views
from carapp import views

app_name='carapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('car_page',views.car_page,name='car_page'),
    path('car',views.car,name='car'),
    path('car_del',views.car_del,name='car_del'),
    path('login_out',views.login_out,name='login_out'),
    path('updata',views.updata_car,name='updata'),



]
