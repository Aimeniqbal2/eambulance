from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .form import RegisterForm, LoginForm

urlpatterns = [
    path('home/', views.home, name='home'),
    path('service/', views.services, name='services'),
    path('welcomeservice/', views.welcomeservice, name='welcomeservice'),
    path('welcomecontact/', views.welcomecontact, name='welcomecontact'),
    path('about/', views.about, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('driver_requests/', views.driver_requests, name='driver_requests'),
    path('base/', views.base_view, name='base'),
    path('register/', views.registerView.as_view(), name='register'),
    path('login/', views.login_View.as_view(redirect_authenticated_user=True, template_name='rapidapp/login.html',
                                            authentication_form=LoginForm, next_page="home"), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('request_ambulance/', views.request_ambulance, name='request_ambulance'),
    path('success/', views.success_page, name='success_page'),
    path('error/', views.error_page, name='error_page'),
    path('profile/', views.profile_view, name='profile'),
    path('passwordchange/', views.password_change_view, name='password_change'),
    path('medical_profile/', views.medical_profile_view, name='medical_profile'),
    path('track/', views.track_view, name='track'),
    path('send_message/', views.send_message_view, name='send_message'),
    path('shop/', views.shop_view, name='shop'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('track_order/', views.track_order, name='track_order'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_success/', views.feedback_success, name='feedback_success'),
 

#  ---------------------------Driver/Emts--------------------------------------------

    path('register_driver/', views.register_driver, name='register_driver'),
    path('login_driver/', views.login_driver, name='login_driver'),
    path('driver_dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('update-emergency-status/<int:request_id>/', views.update_request_status, name='update_emergency_status'),
    
]
