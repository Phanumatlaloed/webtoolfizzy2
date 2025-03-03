from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from django import forms
from .models import Product, Order, Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- เลือกหมวดหมู่สินค้า --"
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image_url']

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # ✅ ลูกค้าสามารถเปลี่ยนสถานะคำสั่งซื้อได้