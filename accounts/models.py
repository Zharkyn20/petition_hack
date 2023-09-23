from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField


class AuthStatusChoices(models.TextChoices):
    CREATED = 'CREATED', 'Новый'
    CONFIRMED = 'CONFIRMED', 'Верифицирован'
    REJECTED = 'REJECTED', 'Отклонен'
    PENDING = 'PENDING', 'На рассмотрении'


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        print(email)
        if not email:
            raise ValueError('Full name is Required')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        print(extra_fields)
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser):
    username = None
    name = models.CharField(max_length=100, verbose_name='Имя')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    inn = models.CharField(max_length=14, verbose_name='ИНН', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)
    auth_status = models.CharField(
        max_length=100,
        choices=AuthStatusChoices.choices,
        verbose_name='Статус аутентификации',
        default=AuthStatusChoices.CREATED,
        blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ['inn', 'full_name']

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserPassportVerificationImages(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='passport_images')
    passport_front = models.ImageField(upload_to='passport_front/', verbose_name='Фото лицевой стороны паспорта')
    passport_selfie = models.ImageField(upload_to='passport_selfie/', verbose_name='Фото с паспортом')
    auth_status = models.CharField(
        max_length=100,
        choices=AuthStatusChoices.choices,
        verbose_name='Статус аутентификации',
        default=AuthStatusChoices.PENDING,
        blank=True, null=True,
        help_text="CREATED - Новый\n"
                  "CONFIRMED - Верифицирован\n"
                  "REJECTED - Отклонен\n"
                  "PENDING - На рассмотрении\n")

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = "Фотографии паспорта для верификации"
        verbose_name_plural = "Фотографии паспортов для верификаций"

    def save(self, *args, **kwargs):
        if self.auth_status == AuthStatusChoices.CONFIRMED:
            self.user.auth_status = AuthStatusChoices.CONFIRMED
        elif self.auth_status == AuthStatusChoices.REJECTED:
            self.user.auth_status = AuthStatusChoices.REJECTED
        self.user.save()
        super().save(*args, **kwargs)
