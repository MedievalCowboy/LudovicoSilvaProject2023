from django.db import transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import Profile, LoginHistory
from .extras import get_client_ip, parse_user_agent

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created.")


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()
        print('Profile updated.')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    with transaction.atomic():
        ip = get_client_ip(request)
        agent_info = parse_user_agent(request)
        
        LoginHistory.objects.create(
            user=user,
            event_type='login',
            ip_address=ip,
            user_agent=agent_info['user_agent'],
            device_type=agent_info['device_type'],
            browser=agent_info['browser'],
            operating_system=agent_info['os']
        )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    with transaction.atomic():
        # Solo registrar logout si el usuario estaba autenticado
        if user.is_authenticated:
            ip = get_client_ip(request)
            agent_info = parse_user_agent(request)
            
            LoginHistory.objects.create(
                user=user,
                event_type='logout',
                ip_address=ip,
                user_agent=agent_info['user_agent'],
                device_type=agent_info['device_type'],
                browser=agent_info['browser'],
                operating_system=agent_info['os']
            )