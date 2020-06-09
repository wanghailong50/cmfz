import os
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect,HttpResponse
from indexapp.models import TBook,TCategory

# Create your views here.


def addemp(request):

     return render(request, 'addEmp.html')


# 头像添加


def add(request):
        product_image_path = request.FILES.get('product_image_path')
        product_image_path.name = str(uuid.uuid4()) + os.path.splitext(product_image_path.name)[1]
        cate_id=request.POST.get('cate_id')   #书籍分类
        book_name = request.POST.get('book_name') #书名
        book_author = request.POST.get('book_author')  #作者
        book_publish = request.POST.get('book_publish')  #出版社
        publish_time = request.POST.get('publish_time') #出版时间
        book_isbn = request.POST.get('book_isbn')  #版号
        word_count = request.POST.get('word_count') # 字数
        page_count = request.POST.get('page_count') #  页数
        open_type = request.POST.get('open_type')  #16开
        book_paper = request.POST.get('book_paper') #纯纸质
        book_wrapper = request.POST.get('book_wrapper') #平装胶订
        book_category = request.POST.get('book_category') #1.0
        book_price = request.POST.get('book_price')  #现价
        book_dprice = request.POST.get('book_dprice')  #原价
        editor_recommendation = request.POST.get('editor_recommendation')  #作者推荐书本
        content_introduction=request.POST.get('content_introduction')  #目录介绍
        author_introduction = request.POST.get('author_introduction') #书作者简介
        media_review=request.POST.get('media_review')  #随意三位数
        # product_image_path=request.POST.get('product_image_path')#图片路径
        printing_time=request.POST.get('printing_time')  #出版时间
        impression=request.POST.get('impression') #一位数
        stock = request.POST.get('stock')  #库存
        shelves_date = request.POST.get('shelves_date') #上架时间
        customer_socre=request.POST.get('customer_socre')  #打折数
        sales = request.POST.get('sales') #销量

        emp = TBook.objects.create(
            impression=impression,
            printing_time=printing_time,
            media_review=media_review,
            content_introduction=content_introduction,
                                   cate_id=cate_id,
                                   book_name=book_name,
                                   book_author=book_author,
                                   book_publish=book_publish,
                                   publish_time=publish_time,
                                   book_isbn=book_isbn,
                                   word_count=word_count,
                                   page_count=page_count,
                                   open_type=open_type,
                                   book_paper=book_paper,
                                   book_wrapper=book_wrapper,
                                   book_category=book_category,
                                   book_price=book_price,
                                   book_dprice=book_dprice,
                                   editor_recommendation=editor_recommendation,
                                   author_introduction=author_introduction,
                                   product_image_path=product_image_path,
                                   sales=sales,
                                   shelves_date=shelves_date,
                customer_socre=customer_socre,
                                   stock= stock,
                                    )
        if emp:
            return HttpResponse('OK')


def index(request):

    books = TBook.objects.all()
    cates1 = TCategory.objects.filter(cate_level=1)
    cates2 = TCategory.objects.filter(cate_level=2)
    books2 = TBook.objects.all()[0:5]
    books3 = TBook.objects.all()[0:10]
    try:
        test = request.session.get('user')
        return render(request, 'index.html',{'books': books, 'cates1': cates1, 'cates2': cates2, 'books2': books2, 'books3': books3,'user':test})
    except:
        pass


def details(request):
    user=request.session.get('user')
    id=int(request.GET.get('id'))    #书籍id2
    print(type(id))
    book=TBook.objects.filter(id=id)[0]  #查到书
    date=str(book.publish_time).format('%Y-%m-%d')

    return render(request,'Book details.html',{'book':book,'date':date,'user':user})


def booklist(requset):
    user = requset.session.get('user')
    # 构造分页器对象
    number=requset.GET.get('number',1)

    list=''
    id=requset.GET.get('id')
    print(id,111)
    t1=TCategory.objects.get(id=id)
    if t1.cate_level==1:
        reslut = TCategory.objects.filter(parent_id=id)
        list1=[]
        for i in reslut:
            list1.append(i.id)
            list=TBook.objects.filter(cate_id__in=list1)
    else:
        list=TBook.objects.filter(cate_id=id)
    cates1 = TCategory.objects.filter(cate_level=1)
    cates2 = TCategory.objects.filter(cate_level=2)

    pagtor = Paginator(list,per_page=2)
    count=pagtor.count
    # 总页数
    nums=pagtor.num_pages
    if number=="0" or nums<int(number):
        number=1
        page = pagtor.page(number)
        pagenumber = pagtor.num_pages
    else:
        page=pagtor.page(number)
        pagenumber=pagtor.num_pages
    return render(requset,'booklist.html',{'cates1':cates1,'cates2':cates2,'page':page,'id':id,'count':count,'pagenumber':pagenumber,'user':user})


def login_out(request):
    rd=redirect('indexapp:index')
    rd.set_cookie('user',max_age=0)
    rd.set_cookie('pwd',max_age=0)
    request.session.flush()
    return rd


def listlogin_out(request):
    id=request.GET.get('id')

    rd=redirect("http://127.0.0.1:8008/index/booklist?id="+id)

    rd.set_cookie('user',1, max_age=0)
    rd.set_cookie('pwd', 1 ,max_age=0)
    try:
        del request.session['is_login']
        del request.session["user"]
    except:
        pass
    return rd


def details_out(request):
    id = request.GET.get('id')
    rd=redirect("http://127.0.0.1:8008/index/details?id="+id)
    rd.set_cookie('user',1, max_age=0)
    rd.set_cookie('pwd', 1 ,max_age=0)

    # del request.session['is_login']
    del request.session["user"]
    return rd


