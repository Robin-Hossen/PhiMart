from django.urls import path

from product import views

urlpatterns = [
    # path('',views.ViewProduct.as_view(),name='product-list'),
    path('',views.ProductList.as_view(),name='product-list'),
    # path('<int:id>/', views.ViewSpecifiProduct.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetails.as_view(), name='product-list'),

    
]