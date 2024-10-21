from datetime import datetime
from .models import MenuItem, Order, Cart, OrderItem
from .serializers import MenuItemSerializer
from .serializers import OrderSerializer
from .serializers import UserSerializer
from .serializers import CartSerializer
from .serializers import OrderItemSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.forms.models import model_to_dict


from enum import Enum


class GroupName(Enum):
    MANAGER = 'Manager'
    DELIVERY_CREW = 'Delivery crew'


def user_in_group(self, group_name):
    """ユーザーが指定されたグループに属しているかを確認するヘルパーメソッド"""
    return self.request.user.groups.filter(name=group_name).exists()
# Create your views here.


def response403():
    return Response(status=status.HTTP_403_FORBIDDEN)


def response404():
    return Response(status=status.HTTP_404_NOT_FOUND)


def is_manager(self):
    return user_in_group(self, GroupName.MANAGER.value)


def is_crew(self):
    return user_in_group(self, GroupName.DELIVERY_CREW.value)


def is_customer(self):
    return not is_manager(self) and not is_crew(self)


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        price = request.query_params.get('price')
        category_id = request.query_params.get('category_id')
        featured = request.query_params.get('featured')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=10)
        page = request.query_params.get('page', default=1)
        menu_items = self.get_queryset()
        if id:
            menu_items = menu_items.filter(id=id)
        if price:
            menu_items = menu_items.filter(price=price)
        if category_id:
            menu_items = menu_items.filter(category__id=category_id)
        if featured:
            menu_items = menu_items.filter(featured=featured)
        if search:
            menu_items = menu_items.filter(title__icontains=search)
        if ordering:
            ordering_field = ordering.split(',')
            menu_items = menu_items.order_by(*ordering_field)
        paginator = Paginator(menu_items, per_page=perpage)
        try:
            menu_items = paginator.page(page)
        except EmptyPage:
            menu_items = []
        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if is_manager(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class MenuItemsSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            menu_item = get_object_or_404(MenuItem, pk=pk)
            serializer = self.get_serializer(menu_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def patch(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            menu_item = get_object_or_404(MenuItem, pk=pk)
            serializer = self.get_serializer(
                menu_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def delete(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            menu_item = get_object_or_404(MenuItem, pk=pk)
            menu_item.delete()
            return Response(status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


# ここは管理画面で権限を割り振る


class GroupsManagerUsersView(
    generics.ListCreateAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        if is_manager(self):
            users = self.get_queryset().filter(
                groups__name=GroupName.MANAGER.value)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def post(self, request):
        if is_manager(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                manager_group = Group.objects.get(name=GroupName.MANAGER.value)
                manager_group.user_set.add(user)
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class GroupsManagerUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    Permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=pk)
            manager_group = Group.objects.get(name=GroupName.MANAGER.value)
            isUserManager = user.groups.filter(
                name=GroupName.MANAGER.value).exists()
            if isUserManager:
                user.groups.remove(manager_group)
                return Response(status=status.HTTP_200_OK)
            return response404()
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class GroupsDeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        if is_manager(self):
            users = self.get_queryset().filter(
                groups__name=GroupName.DELIVERY_CREW.value)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def post(self, request):
        if is_manager(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                crew_group = Group.objects.get(
                    name=GroupName.DELIVERY_CREW.value)
                crew_group.user_set.add(user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class GroupsDeliveryCrewUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    Permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class CartMenuItemsView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            carts = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(carts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return response403()

    def post(self, request):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            id = request.data['menuitem']
            menu_item = get_object_or_404(MenuItem, id=id)
            quantity = request.data['quantity']
            # menu_item.price * quantity
            carts = Cart.objects.filter(user=request.user, menuitem=menu_item)
            if not carts:
                data = {
                    'user_id': request.user.id,
                    'menuitem_id': menu_item.id,
                    'quantity': quantity,
                    'unit_price': menu_item.price,
                    'price': menu_item.price,
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                cart = carts[0]
                cart.quantity += int(quantity)
                cart.price = cart.unit_price * cart.quantity
                cart.save()
                serializer = self.get_serializer(cart)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        return response403()


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        if is_manager(self):
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_crew(self):
            orders = self.get_queryset().filter(delivery_crew=request.user)
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_customer(self):
            orders = self.get_queryset().filter(user=request.user)
            for order in orders:
                order_items = OrderItem.objects.filter(order=order)
                order.order_items = order_items
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return response403()

    def post(self, request):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            # まずCartを確認
            # orderを保存
            carts = Cart.objects.filter(user=request.user)
            if (not carts):
                return Response('Cart is empty',
                                status=status.HTTP_400_BAD_REQUEST)
            total = 0
            for cart in carts:
                total += cart.price
            data = {
                'user_id': request.user.id,
                'date': datetime.now(),
                'status': 0,
                'total': total,
            }
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                order = serializer.save()
                carts = Cart.objects.filter(user=request.user)
            # cartとorderからorder_itemを作って保存
                for cart in carts:
                    order_item_data = {
                        'order': order.id,
                        'menuitem': cart.menuitem.id,
                        'quantity': cart.quantity,
                        'unit_price': cart.unit_price,
                        'price': cart.price,
                    }
                    order_item_serializer = OrderItemSerializer(
                        data=order_item_data)
                    if order_item_serializer.is_valid(raise_exception=True):
                        order_item_serializer.save()
                        cart.delete()

                order.order_items = OrderItem.objects.filter(
                    order=order)
                serializer = self.get_serializer(order)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response403()


class OrdersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    Permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            order = get_object_or_404(Order, pk=pk)
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            pk = kwargs.get('pk')
            order = get_object_or_404(Order, pk=pk)
            order_items = OrderItem.objects.filter(order=order)
            order.order_items = order_items
            serializer = self.get_serializer(order)
            data = serializer.data
            data.order_items = order_items
            return Response(data, status=status.HTTP_200_OK)
        return response403()

    def put(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            order = get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(order, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def patch(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            order = get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return response403()
        if is_crew(self):
            order = get_object_or_404(pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_customer(self):
            return response403()
        return response403()

    def delete(self, request, *args, **kwargs):
        if is_manager(self):
            pk = kwargs.get('pk')
            order = get_object_or_404(Order, pk=pk)
            order.delete()
            return Response(status=status.HTTP_200_OK)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()
