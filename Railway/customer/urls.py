from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [

    path('', views.startpage, name='startpage'),
    path('startpage', views.startpage, name='startpage'),
    path('userhome', views.userhome, name='userhome'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('searchtrain', views.search_trains, name='search_train'),
    path('seatselection', views.seatselection, name='seatselection'),
    path('payment', views.reservationofseat, name='reserve'),
    path('nexuspay', views.nexus, name='nexus'),
    path('bkashpay', views.bkash, name='bkashpay'),
    path('rocketpay', views.rocket, name='rocketpay'),
    path('cardpay', views.card, name='cardpay'),
    path('paymentcheck', views.paymentchecking, name='paymentchecking'),
    path('successful', views.success, name='successful'),
    path('verifyticket', views.verify, name='verify-ticket'),
    path('contactus', views.contactus, name='contact-us'),
    path('accounts', views.accounts, name='accounts')

]
