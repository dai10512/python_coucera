
# flake8: noqa: E501

from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/users/me/', views.UsersUsersMeView.as_view()),
    path('token/login/', views.TokenLoginView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemsSingleView.as_view()),
    path('groups/manager/users', views.GroupsManagerUsersView.as_view()),
    path('groups/manager/users/<int:pk>',
         views.GroupsManagerUsersSingleView.as_view()),
    path('groups/delivery-crew/users', views.GroupsDeliveryCrewUsersView.as_view()),
    path('groups/delivery-crew/users/<int:pk>',
         views.GroupsDeliveryCrewUsersSingleView.as_view()),
    path('cart/menu-items', views.CartMenuItemsView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/<int:pk>', views.OrdersSingleView.as_view()),
]
