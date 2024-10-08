from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_user_info/', views.update_user_info, name='update_user_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:category_type>', views.category, name='category'),
    path('category_summary', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
]
