from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, MarketplaceProfile
from django.db.models.signals import pre_save


# User 모델에 대한 post_save 신호를 받는 receiver
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # User 생성 시 Profile도 생성

        # MarketplaceProfile 확인 및 생성 로직
        existing_profile = MarketplaceProfile.objects.filter(user=instance).first()
        if existing_profile:
            print(f"MarketplaceProfile for user {instance.id} already exists.")
        else:
            print(f"No MarketplaceProfile found for user {instance.id}, creating new one.")
            MarketplaceProfile.objects.create(user=instance)

@receiver(pre_save, sender=MarketplaceProfile)
def check_phone_number(sender, instance, **kwargs):
    # 새로운 MarketplaceProfile의 경우에만 중복 확인
    if not instance._state.adding:
        return

    # phone_number 필드가 있는지 확인 (이 코드는 phone_number 필드가 MarketplaceProfile 모델에 있다고 가정함)
    if hasattr(instance, 'phone_number'):
        # 동일한 phone_number를 가진 다른 MarketplaceProfile 객체가 있는지 확인
        if MarketplaceProfile.objects.filter(phone_number=instance.phone_number).exists():
            raise ValueError(f"MarketplaceProfile with phone number {instance.phone_number} already exists.")

