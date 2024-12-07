from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from sharingit import settings


# Create your models here.
class CustomUser(AbstractUser):
    description = models.TextField(blank=True, verbose_name="Описание")
    about = models.TextField(blank=True, verbose_name="Небольшоеописание")
    is_company = models.BooleanField(default=False, verbose_name="Представитель компании")
    company = models.ForeignKey(
        'companies',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Компания",
        related_name="representatives"
    )
    #
    def __str__(self):
        return self.username
    #photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Membership(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name="Пользователь")
    company = models.ForeignKey('companies', on_delete=models.CASCADE, verbose_name="Компания")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        unique_together = ("user", "company")  # Ограничение: один пользователь в одной компании только один раз

    def __str__(self):
        return f"{self.user.username} -> {self.company.title}"

class companies(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL",null=True,blank=True,)
    content = models.TextField(blank=True, verbose_name="Описание компании",null=True)
    #photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    # time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    # time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    raiting = models.FloatField(default=0,max_length=1, verbose_name="Рейтинг")
    cat = models.ManyToManyField(Category, related_name='companies', verbose_name="Категории",
                                 blank=True)  # Это должно быть ManyToManyField

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'IT компания'
        ordering = ['id']

    def recalculate_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.raiting = reviews.aggregate(models.Avg('rating'))['rating__avg']
        else:
            self.raiting = 0
        self.save()
class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    company = models.ForeignKey(
        'companies',
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Компания"
    )
    content = models.TextField(verbose_name="Отзыв")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user.username} для {self.company.title}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def save(self, *args, **kwargs):
        if Review.objects.filter(user=self.user, company=self.company).exists():
            raise ValidationError("Вы уже оставляли отзыв для этой компании.")
        super().save(*args, **kwargs)