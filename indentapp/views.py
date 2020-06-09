from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from indexapp.models import TAddress,TUser,TShipping,TBook,TOrder,DOrderiterm
import json
# Create your views here.
import uuid


def indent_page(request):
    user=request.session.get('user')
    if user:
        return HttpResponse('1')
    else:
        url=request.GET.get('url')
        request.session['url']=url
        return HttpResponse('0')


def indent(request):
    username = request.session.get('user')
    userid = TUser.objects.filter(username=username)[0].id

    car = TShipping.objects.filter(user_id=int(userid))  # 购物车id  多个商品id

    count = 0
    book_list=[]
    nums=[]
    for i in car:
        book = TBook.objects.filter(id=i.order_id)

        book_list.append({'book_name':book[0].book_name,'publish':book[0].book_publish,'price':book[0].book_price,'num':i.shop_num,'nums':book[0].book_price*i.shop_num,'customer_socre':book[0].customer_socre})
        nums.append(i.shop_num)
        count += float(TBook.objects.get(id=i.order_id).book_price) * float(i.shop_num)

    address = TAddress.objects.all()

    user = request.session.get('user')
    return render(request,'indent.html',{'user':user,'address':address,'count':count,'book_list':book_list})


def indent_out(request):
    rd=redirect("http://127.0.0.1:8008/index/index")
    rd.set_cookie('user',1, max_age=0)
    rd.set_cookie('pwd', 1 ,max_age=0)
    try:
        del request.session['is_login']
        del request.session["user"]
    except:
        pass
    return rd


def indent_ok(request):
    user=request.session.get('user')
    user_id=TUser.objects.get(username=user).id
    result=DOrderiterm.objects.filter(users_id=user_id)[0]
    return render(request,'indent ok.html',{'user':user,'result':result,'username':user})


def address(request):
    user = request.session.get('user')  # 查询该订单属于哪个用户
    user_id = TUser.objects.filter(username=user)[0].id

    # 当用户再次下订单时，需要把之前的订单删除
    if  DOrderiterm.objects.filter(users_id=user_id):
        result = DOrderiterm.objects.filter(users_id=user_id)[0]
        result.delete()

    input_one=request.GET.get('input_one')
    input_two=request.GET.get('input_two')
    input_three=request.GET.get('input_three')
    input_four=request.GET.get('input_four')
    input_five=request.GET.get('input_five')
    addr_id=request.GET.get('addr_id')    #地址id

    result=TAddress.objects.filter(name=input_one,address=input_two,zipcode=input_three,
                            user_id=user_id,phone=input_four,telephone=input_five)

    if  not result:
        TAddress.objects.create(name=input_one, address=input_two, zipcode=input_three,
                                user_id=user_id, phone=input_four, telephone=input_five)
    car = TShipping.objects.filter(user_id=int(user_id))    #     点击提交订单存入订单表数据
    count=0
    nums=0
    book_id=0
    for i in car:
        book = TBook.objects.filter(id=i.order_id)
        book_id=book[0].id

        price= book[0].book_price * i.shop_num     #订单总价
        nums+=i.shop_num                     #项表总数
        count+=book[0].book_price*i.shop_num   #总金额
        order=TOrder.objects.create(t_u_id=user_id,t_a_id=int(addr_id),price=price,order_id=book_id,status=i.shop_num)
        order.save()
    uu=uuid.uuid4()
    print(book_id)
    DOrderiterm.objects.create(price=count,shop_num=nums,users_id=user_id,uuid=uu,shop_bookid=TBook.objects.filter(id=book_id)[0])
    shopping=TShipping.objects.filter(user_id=user_id)   #提交订单之后删除购物车中的数据
    shopping.delete()


    return HttpResponse('1')


def addr_page(request):
    id=request.GET.get('id')

    def user_default(u):
        if isinstance(u,TAddress):
            return {'id':str(u.id),'name':str(u.name),'address':u.address,'zipcode':u.zipcode,'phone':u.phone,'telephone':u.telephone}
    result=TAddress.objects.filter(id=id)
    result=json.dumps(list(result),default=user_default)
    print(result,112)
    return HttpResponse(result)