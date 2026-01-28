 
from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('register/', views.register_view),
    path('product/', views.get_products),
    path('categery/', views.get_categery),
    path('product/<int:pk>/', views.get_product),
    path('cart/', views.get_cart),
    path('cart/add/', views.add_to_cart),
    path('cart/remove/', views.remove_from_cart),
    path('cart/update/', views.update_to_cart),
    path('orders/create/', views.create_order),

    ]
