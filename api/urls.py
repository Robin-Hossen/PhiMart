from django.urls import path,include
from product.views import ProductViewSet,CategoryViewSet,ReviewViewSet,ProductImageViewset
from rest_framework_nested import routers
from order.views import CartViewSet,CartItemViewSet,OrderViewSet

# router=SimpleRouter()
router=routers.DefaultRouter()
router.register('products',ProductViewSet,basename='products')
router.register('categories',CategoryViewSet)
product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product-review')
product_router.register('images',ProductImageViewset,basename='product-images')



router.register('carts',CartViewSet,basename='carts')
cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')

router.register('orders',OrderViewSet,basename='orders')








# urlpatterns = router.urls
urlpatterns =[
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
]