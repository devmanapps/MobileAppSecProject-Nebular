from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, is_admin, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff,
        is_active=True,
        is_superuser=is_superuser,
        is_admin=is_admin,
        last_login=now,
        date_joined=now,
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, True, **extra_fields)
    user.save(using=self._db)
    return user


  def create_admin(self, email, password, **extra_fields):
    user=self._create_user(email, password, False, True, True **extra_fields)
    user.save(using=self._db)
    return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    organization = models.CharField(max_length=254, null=True, blank=False)
    short_name = models.CharField(max_length=254, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['organization']

    objects = UserManager()

    def get_short_name(self):
        return self.short_name

    def get_full_name(self):
        return self.name

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
