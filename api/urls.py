from django.urls import path,include
from product.views import ProductViewSet,CategoryViewSet,ReviewViewSet,ProductImageViewset
from rest_framework_nested import routers
from order.views import CartViewSet,CartItemViewSet,OrderViewSet,initiate_payment,payment_success,payment_cancel,payment_fail,HasOrderedProduct

# router=SimpleRouter()
router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet)
router.register('orders',OrderViewSet,basename='orders')
router.register('carts',CartViewSet,basename='carts')


product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product-review')
product_router.register('images',ProductImageViewset,basename='product-images')




cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')





# urlpatterns = router.urls
urlpatterns =[
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/',initiate_payment,name="initiate-payment"),
    path('payment/success/',payment_success,name="payment-success"),
    path('payment/cancel/',payment_cancel,name="payment-cancel"),
    path('payment/fail/',payment_fail,name="payment-fail"),
    path('orders/has_ordered/<int:product_id>/',HasOrderedProduct.as_view())
    
]