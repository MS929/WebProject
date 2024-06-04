from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Category, Product, Profile, MarketplaceProfile
from .forms import ProductForm, UserForm, ProfileForm, CustomUserCreationForm, MarketplaceProfileForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        MarketplaceProfile.objects.create(user=instance)
    else:
        instance.profile.save()
        if hasattr(instance, 'marketplaceprofile'):
            instance.marketplaceprofile.save()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data['username']
                raw_password = form.cleaned_data['password1']
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            except IntegrityError:
                form.add_error(None, "계정 생성 중 오류가 발생했습니다.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'marketplace/signup.html', {'form': form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'marketplace/home.html', {'products': products})

@login_required
def profile(request):
    user = request.user
    profile = user.profile
    context = {
        'profile': profile,
        'user': user
    }
    return render(request, 'marketplace/profile.html', context)

class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'marketplace/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_name = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(name__icontains=query)
        if category_name:
            queryset = queryset.filter(category__name=category_name)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if q:
            queryset = queryset.filter(title__icontains=q)
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_update.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller

class ProductDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'marketplace/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller

@login_required
def update_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'errors': user_form.errors.as_text() + profile_form.errors.as_text()
            }
            return render(request, 'marketplace/update_profile.html', context)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'marketplace/update_profile.html', context)

from .models import Category

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,user=request.user, categories=Category.objects.all())
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm(user=request.user, categories=Category.objects.all())
        
    return render(request, 'marketplace/product_create.html',{'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance=product, categories=Category.objects.all())
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product, categories=Category.objects.all())
    return render(request, 'product_update.html', {'form': form})

def product_list(request):
    category = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'categories':category,'products': products})

