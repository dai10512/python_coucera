from .models import MenuItem, Order
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
        if user_in_group(self, 'Manager'):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        return Response(status=status.HTTP_403_FORBIDDEN)


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
        if user_in_group(self, 'Manager'):
            menu_item = self.get_object_or_404(MenuItem, pk=pk)
            serializer = MenuItemSerializer(menu_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if user_in_group(self, 'Manager'):
            menu_item = self.get_object_or_404(MenuItem, pk=pk)
            serializer = MenuItemSerializer(
                menu_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if user_in_group(self, 'Manager'):
            menu_item = self.get_object_or_404(MenuItem, pk=pk)
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# ここは管理画面で権限を割り振る


class GroupsManagerUsersView(
    generics.ListCreateAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):
        if user_in_group(self, 'Manager'):
            users = User.objects.filter(groups__name='Manager')
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if user_in_group(self, 'Manager'):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsManagerUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def delete(self, request, pk):
        if user_in_group(self, 'Manager'):
            user = self.get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupsDeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request):
        if user_in_group(self, 'Manager'):
            users = self.queryset.filter(groups__name='DeliveryCrew')
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if user_in_group(self, 'Manager'):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise__exception=True):
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsDeliveryCrewUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def delete(self, request, pk):
        if user_in_group(self, 'Manager'):
            user = self.get_object_or_404(User, pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CartMenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isDeliveryCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isDeliveryCrew
        if isCustomer:
            menu_items = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isDeliveryCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isDeliveryCrew
        if isCustomer:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isManager:
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if isCrew:
            orders = self.get_queryset().filter(delivery_crew=request.user)
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if isCustomer:
            orders = self.get_queryset().filter(user=request.user)
            serializer = self.get_serializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isCustomer:
            serializer = self.get_object_or_404(data=request.data)
            if serializer.isValid(raise_exception=True):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializes_class = OrderSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isManager:
            pass
        if isCrew:
            pass
        if isCustomer:
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        order = self.get.object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        pass

    def put(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isCustomer:
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(order, data=request.data)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isCrew:
            order = self.get_object_or_404(pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
        if isCustomer:
            order = self.get_object_or_404(Order, pk=pk)
            serializer = self.get_serializer(
                order, data=request.data, partial=True)
            if (serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        isManager = user_in_group(self, 'Manager')
        isCrew = user_in_group(self, 'DeliveryCrew')
        isCustomer = not isManager and not isCrew
        if isManager:
            order = self.get_object_or_404(Order, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
