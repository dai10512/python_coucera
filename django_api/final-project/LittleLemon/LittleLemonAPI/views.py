from .models import MenuItem, Order, Cart
from .serializers import MenuItemSerializer, OrderSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404


def user_in_group(self, group_name):
    """ユーザーが指定されたグループに属しているかを確認するヘルパーメソッド"""
    return self.request.user.groups.filter(name=group_name).exists()
# Create your views here.


def response403():
    return Response(status=status.HTTP_403_FORBIDDEN)


def is_manager(self):
    return user_in_group(self, 'Manager')


def is_crew(self):
    return user_in_group(self, 'DeliveryCrew')


def is_customer(self):
    return not is_manager(self) and not is_crew(self)


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

    def get_permissions(self):
        # すべての認証済みユーザーがアクセス可能
        return [IsAuthenticated()]

    def get(self, _):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        if is_manager(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def put(self, request, pk):
        return response403()

    def patch(self, request, pk):
        return response403()

    def delete(self, request, pk):
        return response403()


class MenuItemsSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        # すべての認証済みユーザーがアクセス可能
        return [IsAuthenticated()]

    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, pk):

    def put(self, request, pk):
        if is_manager(self):
            menu_item = get_object_or_404(MenuItem, pk=pk)
            serializer = MenuItemSerializer(menu_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()

    def patch(self, request, pk):
        if is_manager(self):
            menu_item = get_object_or_404(MenuItem, pk=pk)
            serializer = MenuItemSerializer(
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

    def delete(self, request, pk):
        if is_manager(self):
            menu_item = self.get_object_or_404(MenuItem, pk=pk)
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):
        if is_manager(self):
            users = User.objects.filter(groups__name='Manager')
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
                serializer.save()
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

    def get_permissions(self):
        return [IsAuthenticated()]

    def delete(self, request, pk):
        if is_manager(self):
            user = self.get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class GroupsDeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):

        if is_manager(self):
            users = self.queryset.filter(groups__name='DeliveryCrew')
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
            if serializer.is_valid(raise__exception=True):
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

    def get_permissions(self):
        return [IsAuthenticated()]

    def delete(self, request, pk):
        if is_manager(self):
            user = self.get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()


class CartMenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            menu_items = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return response403()

    def post(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response403()


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
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
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return response403()

    def post(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            serializer = self.get_serializer(data=request.data)
            if serializer.isValid(raise_exception=True):
                cart = Cart.objects.filter(user=request.user)
                serializer.save()
                cart.delete()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response403()


class OrdersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializes_class = OrderSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return response403()

    def put(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            return response403()
        if is_customer(self):
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(order, data=request.data)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response403()

    def patch(self, request, pk):
        if is_manager(self):
            return response403()
        if is_crew(self):
            order = self.get_object_or_404(pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if is_customer(self):
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response403()

    def delete(self, request, pk):
        if is_manager(self):
            order = self.get_object_or_404(Order, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if is_crew(self):
            return response403()
        if is_customer(self):
            return response403()
        return response403()
