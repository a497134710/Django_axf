import os
import uuid

from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from axf.models import Wheel, nav, MustBuy, Shop, MainShow, Market, Goods, User, Cart, Order, OrderGoods

# 首页
from axf_python1807 import settings


def home(request):
    wheels = Wheel.objects.all()
    navs = nav.objects.all()
    mustbuy = MustBuy.objects.all()
    shop = Shop.objects.all()
    shop1 = shop[0] # 便利店
    shop2 = shop[1:3] #热销
    shop3 = shop[3:7]
    shop4 = shop[7:11]

    mainobj = MainShow.objects.all()

    data = {
        "wheels":wheels,
        "nav":navs,
        "mustbuy":mustbuy,
        "shop":shop,
        "mainobj":mainobj,
    }
    return render(request,'home.html',context={
        "data":data,
        "wheels":wheels,
        "navs":navs,
        "mustbuy":mustbuy,
        "shop1":shop1,
        "shop2": shop2,
        "shop3": shop3,
        "shop4": shop4,
         "mainobj":mainobj,
    })


def mine(request):
    token = request.session.get("token")
    if token:

        user = User.objects.get(token=token)
        name = user.name
        orders = Order.objects.filter(user=user)
        notpaynum = 0 # 初始化 数量
        paynum = 0

        for order in orders:
            if order.status == 1 :
                notpaynum +=1
            elif order.status == 2 :
                paynum +=1


        data ={
            'user':user,
            'name':name,
            "notpay": notpaynum,
            "pay":paynum,
            "status":1,
        }

        return render(request,'mine.html',context=data)
    else:
        data = {
            "status":0
        }
        return   render(request,'mine.html',context=data)

# 闪购超市
def market(request,categoryid,childid,sortid):
    # 侧边栏数据
    markets = Market.objects.all()
    # 主体商品内容


    typeid = int(request.COOKIES.get('typeIndex',0))

    categoryid =  markets[typeid].typeid

    goods = Goods.objects.filter(categoryid=categoryid)


    childlist =  markets[typeid].childtypenames.split("#")
    list1 = []
    for items in childlist:
            items = items.split(":")
            childict = {"typename":items[0],"id":items[1]}
            list1.append(childict)
    list2 = []
    for i in list1:
        a = i['typename']
        list2.append(a)
    idlist = []
    for i in list1:
        b = i['id']
        idlist.append(b)

    if childid == "0":
        goods = Goods.objects.filter(categoryid=categoryid)
        if sortid == "1":
            goods = Goods.objects.filter(categoryid=categoryid).order_by("price")
        elif sortid == "2":
            goods = Goods.objects.filter(categoryid=categoryid).order_by('-price')
        elif sortid == "3":
            goods = Goods.objects.filter(categoryid=categoryid).order_by("productnum")
    else:
        goods = Goods.objects.filter(categoryid=categoryid,childcid=childid)

        if sortid == "1" :
            goods = Goods.objects.filter(categoryid=categoryid,childcid=childid).order_by("price")
        elif sortid == "2" :
            goods = Goods.objects.filter(categoryid=categoryid,childcid=childid).order_by('-price')
        elif sortid == "3" :
            goods = Goods.objects.filter(categoryid=categoryid,childcid=childid).order_by("productnum")

    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

    data = {
        "markets":markets,
        "goods":goods,
        'categoryid':categoryid,
         "list1":list1,
        'list2':list2,
        "idlist":idlist,
        'childid':childid,
        'sortid':sortid,
        'carts': carts,
    }
    return render(request,'market.html',context = data)


def cart(request):
    token = request.session.get("token")
    if token:
        user = User.objects.get(token=token)

        carts = Cart.objects.filter(user=user).exclude(number=0)

        data ={
            "carts":carts,
        }
        return render(request,'cart.html',context=data)
    else:
        return  render(request,'cart.html')


def login(request):

    if request.method == "POST":
       account = request.POST.get('account')

       password =  request.POST.get('password')

       user = User.objects.filter(account=account).filter(password=password)

       if user.exists():
           user = user.first()
           # 更新token 保证数据安全性


           request.session["token"] = user.token

           return redirect('axf:mine')
       else:
           responseDate={
               "status":0,
           }

           return render(request,'login.html',context=responseDate)



    elif  request.method == "GET":

        return render(request,'login.html')


def register(request):




    if request.method == "POST":
        user = User()
        user.account = request.POST.get('account')
        user.name = request.POST.get('name')
        user.password = request.POST.get('password')
        user.token = str(uuid.uuid5(uuid.uuid4(),'register'))
        user.address = request.POST.get('address')
        user.tel = request.POST.get('tel')
        # 头像  将图片保存在相应的目录位置
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDA_ROOT,imgName)

        file = request.FILES.get('file') # FiLES 方式获得 文件名

        if  user.account == '' or user.password == '' : # 信息为空，提示失败

            return  render(request,'register.html',context={"msg":"注册失败，请填写正确的信息","status":0})
        if file:
            with open(imgPath,mode='wb') as  fp:

                user.img = imgName
                for data in file.chunks():
                    fp.write(data)


        user.save()

        request.session["token"] = user.token


        return  redirect('axf:mine')


    elif request.method =="GET":
     return render(request,'register.html')


def logOut(request):
    logout(request)

    return render(request,'mine.html')


def checkuser(request):
    account = request.GET.get("account")

    user = User.objects.filter(account=account)
    if user.exists():
        responseData = {
            "status":0,
            "account":account,
            "msg":'用户已存在，'
        }

        return JsonResponse(responseData)

    else:
        responseData = {
            "status": 1,
            "account": account,
            "msg": '用户可以注册，'
        }

        return JsonResponse(responseData)




def addcart(request):
    token = request.session.get("token")

    #如果登录
    if  token:

        user = User.objects.get(token=token)
        goodid = request.GET.get("goodid")
        good = Goods.objects.get(pk=goodid)
        carts = Cart.objects.filter(user=user).filter(good=good)

        if carts.exists() : # 如果购物车存在
            cart = carts.first()
            cart.number = cart.number+1
            cart.save()
            data = {
                "status": 1,
                "number":cart.number,
            }


            return JsonResponse(data)
        else:
            cart =  Cart()
            cart.user = user
            cart.good = good
            cart.number = 1
            cart.save()
            data ={
                "status":1,
                "number":cart.number,
            }

            return JsonResponse(data)

    else:
        data={
            "status":0,

        }

        return  JsonResponse(data)


def reducecart(request): # 移出购物车
    goodid = request.GET.get('goodid')
    token = request.session.get("token")
    user = User.objects.get(token=token)
    good = Goods.objects.get(pk=goodid)
    carts = Cart.objects.filter(user=user).filter(good=good)
    cart =carts.first()

    cart.number = cart.number - 1
    cart.save()

    data = {
        "status":1,
        "number":cart.number
    }

    return JsonResponse(data)


def isselect(request): # 是否选中


    cartid = request.GET.get('cartid')

    isselect = request.GET.get("status")


    cart = Cart.objects.get(pk=cartid)

    if isselect == 'false': # 代表选中
        cart.isselect = True
    else:
        cart.isselect = False

    cart.save()
    data = {
        'status':"1",

    }
    return JsonResponse(data)


def isall(request):
    token = request.session.get("token")
    user = User.objects.get(token=token)
    all = request.GET.get("all")

    carts = Cart.objects.filter(user=user).exclude(number=0)

    print(all)
    if all == "true":
        for cart in carts:
            cart.isselect = True
            cart.save()
    else:
        for  cart in carts:
            cart.isselect = False
            cart.save()

    data = {
        "status":1,
    }
    return JsonResponse(data)


def order(request): # 生产订单
    token = request.session.get("token")
    if token:
        user =  User.objects.get(token=token)

        # 生成一个订单
        order = Order()

        order.user = user

        order.order_number = str(uuid.uuid5(uuid.uuid4(),"order"))
        order.save()

        carts = Cart.objects.filter(user=user).filter(isselect=True)
        for cart in carts:
            # 订单商品
            order_goods = OrderGoods()
            order_goods.order = order

            order_goods.goods = cart.good

            order_goods.number = cart.number

            order_goods.save()

            # 移除购物车(每生成一个订单，订单对应的商品从购物车移除)

            cart.delete()

        data = {
            "status":1,
            "msg":"订单生成，状态为付款",
            "orderid":order.id,


        }
        return JsonResponse(data)

    else:

        return JsonResponse({"msg":"用户请登录再操作"})


def ordermain(request): # 订单信息
    order_id = request.GET.get("orderid")
    order = Order.objects.get(pk = order_id)
    sum = 0
    for i in order.ordergoods_set.all():
        price =  i.goods.price * i.number
        sum = sum + price

    data = {
        "order":order,
        "total":sum,
    }
    return  render(request,'order.html',context=data)


def paysuccess(request):

    order_id = request.GET.get("orderid")
    order = Order.objects.get(pk=order_id)
    for i in order.ordergoods_set.all(): # 支付成功 库存少1
        i.goods.productnum -= 1
        i.save()
    order.status = 2
    order.save()
    data ={
        "status":2,

    }
    return JsonResponse(data)


def myorder(request):
    token = request.session.get("token")
    if token : # 如果用户登录才跳转
        user = User.objects.get(token=token)
        orders = Order.objects.filter(user=user)
        data = {
            "orders":orders,
        }

        return render(request,'myorder.html',context=data)
    else:
        return  render(request,'login.html')
