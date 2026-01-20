from django.contrib import admin
from .models import CategoryModel,ProductModel,UserProfileModel,OrderItem,OrderModel
# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(UserProfileModel)
admin.site.register(OrderItem)
admin.site.register(OrderModel)
