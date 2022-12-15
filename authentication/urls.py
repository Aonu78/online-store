from django.urls import path,include
from authentication import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='login'),
    path('logout/',views.handlelogout,name="logout"),
    path('activate/<uidb64>/<token>',views.ActivateAccount.as_view(),name='activate'),
    path('request-email-reset/',views.RequestEmailReset.as_view(),name='request-email-reset'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPassword.as_view(),name='set-new-password'),
    
]
