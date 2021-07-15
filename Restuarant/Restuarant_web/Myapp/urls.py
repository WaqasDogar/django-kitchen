from django.urls import path
from Myapp import views

urlpatterns = [

    #signin and up

    path('signin', views.signin , name='signin'),

    path('signup', views.signup , name='signup'),

    #Logout path

    path('logout', views.logouts, name='logout'),

    #template
    path('',views.temp,name='index'),

    #myadmin side

    path('myadmin',views.myadmin,name='myadmin'),

    path('useraccount/<str:pk>',views.useraccount,name='useraccount'),

    path('deletepro/<str:id>',views.deletepro,name='deletepro'),

    path('updatepro/<str:id>',views.updatepro,name='updatepro'),

     path('addpro/',views.addpro,name='addpro'),

    #cart data--------------------------------
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),

    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),

    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),

    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),

    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),

    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('cart/deletecartitem/<int:id>',views.deletecartitem,name='deletecartitem'),
    #cart buy---------------------------------
    path('store', views.store, name='store'),

    #food approvel

    path('Approve/<str:id>/<str:name>', views.approve, name='Approve'),

    path('Reject/<str:id>/<str:name>', views.reject, name='Reject'),

]