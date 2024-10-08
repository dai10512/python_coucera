from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.Menu_items.as_view()),
    # path('groups/manager/users', views.menu_items.as_view()),
    # path('groups/manager/users/<int:pk>', views.menu_items.as_view()),
    # path('groups/delivery-crew/users', views.menu_items.as_view()),
    # path('groups/delivery-crew/users/<int:pk>', views.menu_items.as_view()),
    path('cart/menu-items', views.menu_items.as_view()),
    path('orders', views.menu_items.as_view()),
    path('orders/<int:pk>', views.menu_items.as_view()),
]
