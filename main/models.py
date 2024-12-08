from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

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
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото",null=True,blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
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
        # Получение всех заказов компании
        orders = self.order.all()
        # Сбор всех отзывов, связанных с заказами
        reviews = Review.objects.filter(order__in=orders)
        # Расчет среднего рейтинга
        if reviews.exists():
            self.raiting = sum(review.rating for review in reviews) / reviews.count()
        else:
            self.raiting = 0

        self.save()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании ответа компании'),
        ('accepted', 'Принят компанией'),
        ('declined', 'Отклонен компанией'),
        ('completed_on_time', 'Выполнен в срок'),
        ('completed_late', 'Выполнен, но с нарушением сроков'),
        ('not_completed', 'Не выполнен'),
        ('rejected_by_client', 'Заказчик отказался принимать работу'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="orders"
    )
    company = models.ForeignKey(
        'companies',
        on_delete=models.CASCADE,
        related_name="order",
        verbose_name="Компания"
    )
    description = models.TextField(verbose_name="Описание заказа")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    delivery_time = models.DateTimeField(
        verbose_name="Время сдачи",
        null=True,
        blank=True,
        help_text="Дата и время завершения заказа"
    )

    def __str__(self):
        return f"Заказ от {self.user.username} для {self.company.title}"

    def save(self, *args, **kwargs):
        # Если статус меняется на выполненный, записать текущую дату и время
        if self.status in ['completed_on_time', 'completed_late'] and not self.delivery_time:
            self.delivery_time = now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="reviews",
        null=True,  # Позволяет хранить null в базе данных
        blank=True  # Делает поле необязательным для заполнения в формах
    )
    content = models.TextField(verbose_name="Отзыв")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"