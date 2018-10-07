from django.db import models

# Create your models here.

class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

# 轮播图
class  Wheel(Base):
# 轮播图数据
# 模型名称 Wheel  (在生成表时，就是axf_wheel)
# 模型属性 img,name,trackid

    name = models.CharField(max_length=20)
    img  = models.CharField(max_length=100)
    trackid = models.CharField(max_length=10)


    class Meta:
        db_table = "axf_wheel"
# 导航栏
class  nav(Base):

    class Meta:
        db_table = "axf_nav"



# 每日必抢

class MustBuy(Base):

    class Meta:
        db_table = "axf_mustbuy"

# 便利店

class  Shop(Base):
    class Meta:
        db_table ='axf_shop'


# 优选类
class  MainShow(models.Model):

    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=100)
    marketprice1 = models.CharField(max_length=100)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=100)
    marketprice2 = models.CharField(max_length=100)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=100)
    marketprice3 = models.CharField(max_length=100)


# 闪购超市

class Market(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=15)
    childtypenames = models.CharField(max_length=200)
    typesort = models.CharField(max_length=30)


    class Meta:
        db_table = "axf_foodtypes"


class  Goods(models.Model):

    productid = models.CharField(max_length=10)
    productimg = models.CharField(max_length=100)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=20)
    price = models.IntegerField()
    marketprice = models.IntegerField()
    # 分类id
    categoryid = models.IntegerField()
    # 子类id
    childcid = models.IntegerField()
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=20)
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'

class User(models.Model):
    account = models.CharField(max_length=12,unique=True)

    password = models.CharField(max_length=200)

    tel = models.CharField(max_length=20)

    img = models.CharField(max_length=100)

    name = models.CharField(max_length=30)


    address = models.CharField(max_length=50)

    token = models.CharField(max_length=100)


# 购物车

class  Cart(models.Model):

    user = models.ForeignKey(User)

    good = models.ForeignKey(Goods) # 将user和goods关联 关联关系多对多

    number = models.IntegerField(default=1)

    isselect = models.BooleanField(default=True) # 默认选中

# 订单 模型类

# 一个用户对于多个订单



class  Order(models.Model):

    order_number = models.CharField(max_length=256)

    user = models.ForeignKey(User)

    #状态
    # 1. 未付款
    # 2. 已付款，未发货
    # 3. 已发货，未收货
    # 4. 已收货，未评价
    # 5. 已评价
    # 6. 退款

    status = models.IntegerField(default=1)


    # 订单生成的时间

    createtime = models.DateTimeField(auto_now=True)



# 订单商品

class  OrderGoods(models.Model):

    # 订单

    order =  models.ForeignKey(Order)

    goods =  models.ForeignKey(Goods)

    # 数量
    number = models.IntegerField(default=1)















