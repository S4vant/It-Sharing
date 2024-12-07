from .models import Article
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea



class ArticleForm(ModelForm): #Форма для нвовости
    class Meta:
        model = Article
        fields = ['title', 'anons', 'full_text']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок новости'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс новости'
            }),

            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст новости'
            })
        }