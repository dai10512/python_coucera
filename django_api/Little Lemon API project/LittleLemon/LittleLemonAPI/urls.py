
# flake8: noqa: E501

from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemsSingleView.as_view()),
    path('groups/manager/users/', views.GroupsManagerUsersView.as_view()),
    path('groups/manager/users/<int:pk>/',
         views.GroupsManagerUsersSingleView.as_view()),
    path('groups/delivery-crew/users/',
         views.GroupsDeliveryCrewUsersView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/',
         views.GroupsDeliveryCrewUsersSingleView.as_view()),
    path('cart/menu-items/', views.CartMenuItemsView.as_view()),
    path('orders/', views.OrdersView.as_view()),
    path('orders/<int:pk>/', views.OrdersSingleView.as_view()),
]
