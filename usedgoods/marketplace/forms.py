from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from .models import Product, Profile, MarketplaceProfile, Category
from marketplace.models import Category  


User = get_user_model()

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none())

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'seller','image','category']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        categories = kwargs.pop('categories', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['seller'].queryset = User.objects.filter(id=user.id)
        if categories is not None:
            self.fields['category'].queryset = categories
        else:
            self.fields['category'].queryset = Category.objects.all()
            
class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = '전화번호'

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, label='전화번호')

    username = forms.CharField(
        help_text='<span class="help-text">150자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.</span>'
    )
    
    password2 = forms.CharField(
        help_text='<span class="help-text">확인을 위해 이전과 동일한 비밀번호를 입력하세요.</span>',
        label='비밀번호 확인',
        widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone_number"]

    def save(self, commit=True):
        try:
            user = super(CustomUserCreationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                phone_number = self.cleaned_data['phone_number']
                Profile.objects.create(user=user, phone_number=phone_number)
                
                if not MarketplaceProfile.objects.filter(user=user).exists():
                    MarketplaceProfile.objects.create(user=user, phone_number=phone_number)
                else:
                    # 이미 존재하는 경우 처리
                    pass
            return user
        except IntegrityError as e:
            # 데이터베이스 무결성 오류 처리
            pass

class MarketplaceProfileForm(forms.ModelForm):
    class Meta:
        model = MarketplaceProfile
        fields = ['phone_number']  # 필요한 필드들 추가

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if MarketplaceProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("이미 존재하는 전화번호입니다.")
        return phone_number