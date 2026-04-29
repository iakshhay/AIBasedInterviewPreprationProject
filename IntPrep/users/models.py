from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

    def __str__(self):
        return self.email
    
class Skill(models.Model):
    name=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    TARGET_ROLES=(
        ("backend","Backend"),
        ("frontend","Frontend"),
        ("full_stack","Full stack")
    )

    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    target_role=models.CharField(max_length=20,choices=TARGET_ROLES)
    target_companies=models.CharField(max_length=255,blank=True)
    skills=models.ManyToManyField(Skill,related_name='profiles',blank=True)

    def __str__(self):
        return self.user.email