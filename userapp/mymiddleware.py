from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from indexapp.models import TUser


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)

    # view处理请求前执行
    def process_request(self, request):
        # 某一个view
        if '/indent/indent' in request.path or 'indent/indent_ok' in request.path :

            referer=request.META.get("HTTP_REFERER")
            if not referer:
                return redirect('indexapp:index')
        else:
            user=request.COOKIES.get('user')   #获取login函数设置的cookies
            pwd=request.COOKIES.get('pwd')
            result=TUser.objects.filter(username=user,password=pwd)   #查询是否有cookies种存的这个用户，如果有，直接登陆
            if result:
                request.session['is_login']=True #有cookies需要存一个登陆状态，， 存一个用户名在session中
                request.session['user']=user

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        pass
