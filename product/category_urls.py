from django.urls import path

from product import views

urlpatterns = [
    path('<int:pk>/',views.ViewSpecificCategories.as_view(),name='view_specific_category'),
    path('',views.ViewCategories.as_view(),name='category-list')
]