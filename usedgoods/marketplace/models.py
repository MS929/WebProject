from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission

def get_default_user():
    User = settings.AUTH_USER_MODEL
    user, created = User.objects.get_or_create(username='defaultuser')
    return user.id

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='판매자')
    title = models.CharField('제목', max_length=100)
    description = models.TextField('설명')
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField('사진',upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='카테고리')

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class MarketplaceProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_default_user)
    phone_number = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.user.username

    def clean(self):
        if MarketplaceProfile.objects.filter(phone_number=self.phone_number).exclude(pk=self.pk).exists():
            raise ValidationError("이미 존재하는 전화번호입니다.")

class Category(models.Model):
    name = models.CharField('카테고리', max_length=50)

    def __str__(self):
        return self.name

