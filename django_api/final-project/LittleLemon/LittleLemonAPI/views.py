from typing import Any, List
from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer, UserSerializer
from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import permissions

# Create your views here.


def get_permissions(
    method: str,
    get: List[Any],
    post: List[Any],
    put: List[Any],
    patch: List[Any],
    delete: List[Any]
):
    permissions_map = {
        'GET': get,
        'POST': post,
        'PUT': put,
        'PATCH': patch,
        'DELETE': delete
    }
    return permissions_map.get(method, [])


class IsManager(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.user.groups.filter(name='Manager').exists():
            return True
        return False


class IsCrew(permissions.BasePermission):

    def has_permission(self, request, _):
        if request.user.groups.filter(name='DeliveryCrew').exists():
            return True
        return False


class MenuItemsView(
    # get
    generics.ListAPIView,
    # post
    generics.CreateAPIView,
    # put patch
    generics.UpdateAPIView,
    # delete
    generics.DestroyAPIView
):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class MenuItemsSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class GroupsManagerUsersView(
    generics.ListCreateAPIView,
    generics.CreateAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class GroupsManagerUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
#         return permission
#


class GroupsDeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class GroupsDeliveryCrewUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class CartMenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission


class OrdersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializes_class = OrderSerializer

    # def get_permissions(self):
    #     permission = get_permissions(
    #         method=self.request.method,
    #         get=[],
    #         post=[IsManager()],
    #         put=[IsManager()],
    #         patch=[IsManager()],
    #         delete=[IsManager()],
    #     )
    #     return permission
