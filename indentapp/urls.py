
from django.contrib import admin
from django.urls import path,include
from indexapp import views
from indentapp import views

app_name='indentapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('indent_page',views.indent_page,name='indent_page'),
    path('indent',views.indent,name='indent'),
    path('indent_out',views.indent_out,name='indent_out'),
    path('indent_ok',views.indent_ok,name='indent_ok'),
    path('address',views.address,name='address'),
    path('addr_page',views.addr_page,name='addr_page'),



]
