from django.db import models



class Article(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публликации', auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'