from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name = 'landing_page'),
    path('login/',views.handlelogin, name='handlelogin'),
    path('signup/',views.handle_signup, name='signup'),
    path('logout/',views.handlelogout, name='logout'),
    path('about/',views.about, name='about'),
]