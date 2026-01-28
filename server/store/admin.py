from django.contrib import admin
from .models import CategoryModel,ProductModel,UserProfileModel,OrderItemModels,OrderModel
# Register your models here.

admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(UserProfileModel)
admin.site.register(OrderItemModels)
admin.site.register(OrderModel)
