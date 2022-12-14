from datetime import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        if not email:
            raise ValueError('The email must be set.')
        if not username:
            raise ValueError('The username must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email, username, **extra_fields):
        user = self.create_user(email, username, **extra_fields)
        user.role = user.UserRole.ADMIN
        user.save()
        return user

    def create_staff(self, email, username, **extra_fields):
        user = self.create_user(email, username, **extra_fields)
        user.role = user.UserRole.MODERATOR
        user.save()
        return user


class User(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.TextField(max_length=500, null=True, blank=True,
                           verbose_name='Bio')
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=13,
                            choices=UserRole.choices,
                            default=UserRole.USER,
                            verbose_name='Role')
    confirmation_code = models.CharField(max_length=50, null=True,
                                         verbose_name='Confirmation code')

    REQUIRED_FIELDS = ['username']

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR


class Categories(models.Model):
    name = models.CharField(verbose_name='Category name',
                            max_length=200)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genres(models.Model):
    name = models.CharField(verbose_name='Genre name', max_length=200)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Titles(models.Model):
    name = models.CharField(verbose_name='Title',
                            max_length=100)
    year = models.IntegerField(blank=True, null=True,
                               validators=[
                                   MinValueValidator(1600),
                                   MaxValueValidator(datetime.now().year)])
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 null=True, related_name='category',
                                 blank=True)
    genre = models.ManyToManyField(Genres, related_name='genre', blank=True)
    description = models.TextField(max_length=300, blank=True)


class Meta:
    verbose_name = 'Title'
    verbose_name_plural = 'Titles'


class Reviews(models.Model):
    text = models.TextField(verbose_name='Text')
    pub_date = models.DateTimeField(verbose_name='Publication date',
                                    auto_now_add=True)
    score = models.IntegerField(verbose_name='Rating',
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(10))
                                )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Titles, on_delete=models.CASCADE,
                              related_name='reviews')

    class Meta:
        unique_together = ('author', 'title')
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comments(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
