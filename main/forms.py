
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import companies, Category
from .models import *

class CustomUserCreationForm(UserCreationForm): #форма создания нового кастомного пользователя

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','email')

class CustomUserEditForm(ModelForm): #форма изменения кастомного пользователя
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'about', 'description']  # Ука


class RegisterUserForm(CustomUserCreationForm): #форма регистрациии нового кастомого пользователя
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form'}))
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class LoginUserForm(AuthenticationForm): #форма аунтифателя пользователя
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AddPostForm(forms.ModelForm): #Нужная штука
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = companies
        fields = ['title', 'content', 'is_active', 'raiting', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class CompanyForm(forms.ModelForm):# форма для компании
    class Meta:
        model = companies
        fields = ['title', 'content', 'cat']  # Указываем поля, которые будут в форме
        widgets = {
            'cat': forms.CheckboxSelectMultiple(),  # Это создаст поле для выбора нескольких категорий
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Для поля 'content' создаём многострочное поле
            'raiting': forms.NumberInput(attrs={'max': 5, 'min': 0, 'step': 0.1}),  # Поле для рейтинга с ограничениями
        }
        labels = {
            'title': 'Название компании',
            'content': 'Описание компании',
            'raiting': 'Рейтинг компании',
            'cat': 'Категории компании',
        }
        help_texts = {
            'raiting': 'Введите рейтинг от 0 до 5',
        }

    # Если нужно, можно добавить дополнительную валидацию для поля rating (например, чтобы он не был больше 5)
    def clean_raiting(self):
        raiting = self.cleaned_data.get('raiting')
        if raiting > 5:
            raise forms.ValidationError("Рейтинг не может быть больше 5")
        return raiting


class CompanyFilterForm(forms.Form): #Форма фильтра компаний
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категории",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    min_rating = forms.FloatField(
        required=False,
        label="Минимальный рейтинг",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    is_active = forms.BooleanField(
        required=False,
        label="Только активные компании",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
class ReviewForm(forms.ModelForm): #форма для отзывов о компаниии
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Проверка на выбранную компанию, если это необходимо
        if 'company' in self.initial:
            company = self.initial['company']
            if not company:
                raise ValidationError("Компания не может быть пустой")