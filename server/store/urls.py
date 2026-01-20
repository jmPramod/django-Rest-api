 
from django.urls import path,include
from . import views 
urlpatterns = [
    path('product/', views.get_products),
    path('categery/', views.get_categery),
    path('product/<int:pk>/', views.get_product),
    path('cart', views.get_cart),
    path('cart/add/', views.add_to_cart),
    path('cart/remove/', views.get_remove_cart),
    
    ]
