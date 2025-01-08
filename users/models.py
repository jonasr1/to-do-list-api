import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username:str, password:str, **extra_fields): # type: ignore
        if not username:
            raise ValueError("The username is required and cannot be blank.")
        if not password:
            raise ValueError("The password is required and cannot be blank.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Criptografando a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str, **extra_fields): # type: ignore
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username=username, password=password, **extra_fields)
    

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects: MyUserManager = MyUserManager() #type: ignore

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.username