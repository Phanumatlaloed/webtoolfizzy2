from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='ecommerce_users',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='ecommerce_users_permissions',
        blank=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ✅ เพิ่ม FK ไปยัง Category
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

class Order(models.Model):
    STATUS_CHOICES = (
        ('preparing', 'กำลังเตรียมสินค้า'),
        ('ready', 'พร้อมรับสินค้า'),
        ('completed', 'สำเร็จ'),
        ('cancelled', 'ยกเลิก')
    )

    PAYMENT_METHODS = (
        ('transfer', 'โอนเงิน'),
        ('cash', 'เงินสด'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preparing')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    slip_image = models.ImageField(upload_to='slips/', blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
