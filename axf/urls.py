from django.conf.urls import urlfrom axf import viewsurlpatterns=[    url(r'^$',views.home,name='home'),    url(r'^home/$',views.home,name='home'),    url(r'^mine/$', views.mine, name='mine'),    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),    url(r'^cart/$', views.cart, name='cart'),    url(r"^login/$",views.login,name='login'),    url(r'^register/$',views.register,name='register'),    url(r"^logout/$",views.logOut,name='logout'),    url(r"^checkuser/$",views.checkuser,name='checkuser'), # 验证账户    # url(r"^checkpassword/$",views.checkpassword,name='checkpassword')    url(r"^addcart/$",views.addcart,name="addcart"), # 添加到购物车    url(r"^reducecart/$",views.reducecart,name='reducecart'), # 移除购物车    url(r"^isselect/$",views.isselect,name="isselect"), # 是否选中    url(r"^isall/$",views.isall,name='isall'), # 是否全选    url(r"^order/$",views.order,name="order"),   #生产订单    url(r"^ordermain/$",views.ordermain,name='ordermain'), # 订单信息界面    url(r"^paysuccess/$",views.paysuccess,name="paysuccess"), # 付款成功    url(r'^myorder/$',views.myorder,name='myorder'), # 我的订单]