from django.urls import path,include
from shop import views
urlpatterns = [
    path('',views.home,name='home'),
    path('purchase',views.purchase,name='purchase'),
    path('checkout/',views.checkout,name='checkout'),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
    path('tracker/',views.tracker,name='tracker'),
    path('paypal-return', views.paypal_return, name="paypal-return"),
    path('paypal-cancel',views.paypal_cancel,name='paypal-cancel'),
]
