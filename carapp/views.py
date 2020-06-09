from django.shortcuts import render, HttpResponse, redirect
from indexapp.models import TBook,TShipping,TUser
# Create your views here.
import json


class Book:
    def __init__(self,id,num):
        book=TBook.objects.get(id=id)
        self.id=id
        self.picture=book.product_image_path
        self.name=book.book_name
        self.price=book.book_price
        self.num=num


def car_page(request):
    books=request.session.get('car')
    user = request.session.get('user')#注册时需要获取前段传过来了的用名名，如果有，就说明用户注册成功，且登陆成功
    if not user:  #未登录状态
        if books:
            carlist=books.book_itmes
            booklist=[]
            count=0
            for book  in carlist:
                nums=book.num*book.price
                count+=book.num*book.price
                booklist.append({'book':book,'nums':nums})

            return render(request, 'car.html', {'booklist': booklist, 'user': user,'count':count})
        else:
            return render(request, 'car.html', {'user': user,})
    else:                                  #登陆状态
        userid = TUser.objects.get(username=user).id  #查询到用户id
        ord=request.session.get('car')
        if ord:
            carlist=ord.book_itmes
            for book in carlist:
                TShipping.objects.create(user_id=userid,order_id=book.id,shop_num=book.num)
            del request.session["car"]    #添加后需要把购物车中的商品删除
        shoppings = TShipping.objects.filter(user_id=int(userid))  #通过用户id查询购物车的多个商品
        if shoppings:
            count = 0
            booklist=[]
            for book1 in shoppings:
                book=TBook.objects.get(id=book1.order_id)     #查询到购物车中的书的对象
                price=book.book_price #查询到书的单价
                nums=book1.shop_num*price    #计算出每本书的总价
                count += book1.shop_num * price
                bo=Book(book1.order_id,book1.shop_num)      #必须传Book对象到前端，
                booklist.append({'book':bo,'nums':nums})
            return render(request,'car.html',{'booklist':booklist,'user':user,'count':count})
        else:
            return render(request,'car.html',{'user':user})


class Car:
    def __init__(self):
        self.book_itmes = []

    def add_book(self,id,num=0):
        book=self.get_book(id)
        if book:
            book.num+= num

        else:
            book=Book(id,num)
            self.book_itmes.append(book)

    def del_book(self,id):
        book=self.get_book(id)
        if book:
            self.book_itmes.remove(book)

    def get_book(self,id):
        for book in self.book_itmes:
            print(book.id,id,type(book.id),type(id),80)
            if id==book.id:
                print(book,81)
                return book

    def updata_num(self,id,num):
        book=self.get_book(id)
        if book:
            book.num=num


def car(request):
    if not request.session.get('is_login'):  #未登录状态
        id = request.POST.get('id')
        num = int(request.POST.get('num'))

        car = request.session.get('car')
        if car:
            car.add_book(id, num)
            request.session['car'] = car
        else:
            car = Car()
            car.add_book(id, num)
            request.session['car'] = car
        return HttpResponse('0')
    else:                                      #登陆状态
        id = int(request.POST.get('id'))   #书的id
        num = int(request.POST.get('num')) #书的数量
        user=request.session.get('user')   #用户名

        user_id=TUser.objects.get(username=user).id  #查询到用户名的id，，为加入商品做准备

        if TShipping.objects.filter(user_id=user_id,order_id=id):
            tshopping1=TShipping.objects.get(user_id=user_id,order_id=id)
            tshopping1.shop_num+=num
            tshopping1.save()
        else:
            user_id = TUser.objects.get(username=user).id
            TShipping.objects.create(user_id=user_id, shop_num=num, order_id=id)  # 用户id  书籍数量  书籍id
        return HttpResponse('1')


def car_del(request):
    if not request.session.get('is_login'):    #未登陆状态   删除
        id=request.GET.get('id')
        print(id, type(id))
        car=request.session.get('car')
        car.del_book(str(id))
        request.session['car']=car
        return HttpResponse('1')
    else:
        id = int(request.GET.get('id'))    #登陆状态
        print(id)
        username=request.session.get('user')
        user_id=TUser.objects.get(username=username).id
        if TShipping.objects.filter(user_id=user_id,order_id=id):
            del_book=TShipping.objects.filter(user_id=user_id, order_id=id)[0]
            del_book.delete()

            return HttpResponse('1')
        else:
            return HttpResponse('0')


def login_out(request):
    request.session.flush()
    return redirect('carapp:car_page')


def updata_car(request):
    new_num=request.GET.get('num')
    id=request.GET.get('id')
    car = request.session.get('car')
    if not request.session.get('is_login'):   #未登录，更新session的num
        if not car:
            request.session['car']=Car()
        car=request.session.get('car')
        car.updata_num(id,int(new_num))
        request.session['car'] = car    #获取前段的session值

        count=0
        for i in car.book_itmes:     #取出session列表中的Book对象
            price=i.price         #查到每本书的单价
            count+=float(price)*int(i.num)    #每本书的本数

        def user_default(u):           #序列化成前段可识别的对象
            return {'id':count}
        result = json.dumps(str(count), default=user_default)

        return HttpResponse(result)
    else:
        username=request.session.get('user')  #登陆状态更新购物车
        user_id=TUser.objects.get(username=username).id    #查到用户id
        if TShipping.objects.filter(order_id=id,user_id=user_id):   #通过用户id查询用户对应的购物车中的数据   order_id(书对应的id)
            new_thsipping=TShipping.objects.get(order_id=id, user_id=user_id)
            new_thsipping.shop_num=new_num
            new_thsipping.save()

            booklist=TShipping.objects.filter(user_id=user_id)
            count=0
            for book in booklist:
                print(TBook.objects.get(id=book.order_id).book_price)   #查询每本书的单价
                print(book.shop_num)                        #查询每个对象有几本书
                count+=float(book.shop_num)*float(TBook.objects.get(id=book.order_id).book_price)   #总价

            def user_default(u):  # 序列化成前段可识别的对象
                return {'id': count}
            result = json.dumps(str(count), default=user_default)    #序列化  前段需要eval（）转化
            return HttpResponse(result)



