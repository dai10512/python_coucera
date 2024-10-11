from django.db import models


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    category = models.ForeignKey(to=Category,
                                 on_delete=models.PROTECT, default=1)  # 外部キー
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.SmallIntegerField()

    def __str__(self):
        return self.title
