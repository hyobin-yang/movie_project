from django.db import models
# from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
# class CustomUser(AbstractUser):
#     password = models.CharField(max_length=128)
#     nickname = models.CharField(max_length=100)
#     university = models.CharField(max_length=50)

# class CustomUser(AbstractUser):
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name='groups',
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     related_name='customuser_groups'
    # )
    
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name='user permissions',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_name='customuser_permissions'
    # )


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = models.EmailField(null=True)
    nickname = models.CharField(max_length=100, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_groups'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_permissions'
    )
