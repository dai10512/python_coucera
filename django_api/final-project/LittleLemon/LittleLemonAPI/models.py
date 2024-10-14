from django.db import models
from django.contrib.auth.models import User

# Create your views here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return str(self.id) + ':' + self.title


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT)
    ordering_fields = ['id', 'title', 'price', 'featured']  # 順序

    def __str__(self):
        return str(self.id) + ':' + self.title


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuitem')

    def __str__(self):
        username = self.user.username
        menu_title = self.menuitem.title
        return str(self.id) + ':' + username + '-' + menu_title


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    delivery_crew = models.ForeignKey(
        User,
        related_name='delivery_crew',
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.IntegerField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(db_index=True)

    def __str__(self):
        return str(self.id) + ':' + self.user.username + '-' + str(self.date)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
        username = self.order.user.username
        menu_title = self.menuitem.title
        return str(self.id) + ':' + username + '-' + menu_title
