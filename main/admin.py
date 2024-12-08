from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserEditForm
from .models import CustomUser
from django.contrib import admin
from .models import Category, companies

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserEditForm
    model = CustomUser
    list_display = ['email', 'username','description','company']

admin.site.register(CustomUser, CustomUserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_active',)
    filter_horizontal = ('cat',)  # Добавьте это для удобного выбора категорий
    model = companies

admin.site.register(Category)
admin.site.register(companies, CompanyAdmin)