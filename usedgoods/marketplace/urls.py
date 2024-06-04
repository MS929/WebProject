from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import ProductList, ProductCreate, ProductUpdate, ProductDelete,update_profile
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='marketplace/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('product/new/', views.product_create, name='product_create'),  # Function-based 
    path('path/to/product_create/', views.product_create, name='product_create'),
    path('product/add/', ProductCreate.as_view(), name='product_add'),  # Class-based view
    path('product/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
    path('accounts/profile/', views.profile, name='profile'),  # 프로필 페이지 URL 패턴
    path('update_profile/', views.update_profile, name='update_profile'),
    path('product/create/', views.product_create, name='product_create'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)