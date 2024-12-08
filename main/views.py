from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from .models import companies

from .forms import *
from .utils import *

# Create your views here.
#Вывод главной страницы
def index(request):
    data = {
        'title': 'Главная страница',
    }
    return render(request, 'main/index.html', data)

#вывод профиля пользователя
def PersonalPage(request):
    user = request.user
    if user.is_authenticated and user.is_company:
        user_companies = companies.objects.filter(representatives=user)
    else:
        user_companies = None
    data = {
        'title': 'Личный кабинет'
    }
    return render(request, 'main/PersonalPage.html', data)
#Вывод формы измения профиля пользователя
def edit_profile(request):
    user = request.user  # Текущий пользователь
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)  # Редактируем текущего пользователя
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('PersonalPage')  # Перенаправляем, например, на страницу профиля
    else:
        form = CustomUserEditForm(instance=user)  # Загружаем форму с текущими данными пользователя
    return render(request, 'main/PersonalPage_edit.html', {'form': form})
def company_list(request):#вывод списка компаний
    companies_queryset = companies.objects.all()

    # Фильтрация
    form = CompanyFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('category'):
            # Фильтрация по нескольким категориям
            companies_queryset = companies_queryset.filter(cat__in=form.cleaned_data['category'])
        if form.cleaned_data.get('min_rating') is not None:
            companies_queryset = companies_queryset.filter(raiting__gte=form.cleaned_data['min_rating'])
        if form.cleaned_data.get('is_active'):
            companies_queryset = companies_queryset.filter(is_active=True)

    return render(request, 'main/company.html', {
        'companies': companies_queryset,
        'form': form,
    })
#Изменение профиля компаниии
def edit_company(request, company_id):
    # Получаем компанию по ID
    user = request.user  # Текущий пользователь
    company = get_object_or_404(companies, id=company_id)
    if not user.is_authenticated or not user.is_company or user.company != company and not user.is_superuser:
        raise ValidationError("Вы не можете редактировать компанию.")

    # Обработка POST-запроса для сохранения изменений
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', company_id=company.id)  # Перенаправление после сохранения
    else:
        form = CompanyForm(instance=company)

    return render(request, 'main/edit_company.html', {'form': form, 'company': company})
 #Вывод Профиля компании
def company_detail(request, company_id):
    company = get_object_or_404(companies, id=company_id)
    reviews = Review.objects.filter(order__company=company)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.company = company
            review.save()
            company.recalculate_rating()
            return redirect('company_detail', company_id=company.id)

    return render(request, 'main/company_detail.html', {
        'company': company,
        'reviews': reviews,
        'form': form,
    })
# class CreateOrder(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = OrderForm
#     template_name = 'main/create_order.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('home')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Добавление компани")
#         return dict(list(context.items()) + list(c_def.items()))

def create_order(request, company_id):
    if request.user.is_authenticated:
        user = request.user
        company = get_object_or_404(companies, id=company_id)
        # Проверка, существует ли выбранная компания
        if request.method == "POST":
            # Здесь код для обработки создания заказа
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = user
                order.company = company
                order.status =  'pending'
                order.save()
                return redirect('order_detail', order.id)

        else:
            form = OrderForm()

        return render(request, 'main/create_order.html', {'form': form, 'company': company})
    else:
        return redirect('login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderForm(request.POST)
    # company = get_object_or_404(companies, id=company_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "accept":
            # Логика для "Одобрить"
            order.status = 'completed'
        elif action == "denied":
            # Логика для "Отклонить"
            order.status = 'declined'
        order.save()
        return redirect('order_detail', order.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Заказ")
        return dict(list(context.items()) + list(c_def.items()))

    return render(request, 'main/order_detail.html', {'order': order})

def see_orders(request, company_id):
    # Получаем компанию по ID
    company = get_object_or_404(companies, id=company_id)

    # Проверяем, что текущий пользователь является владельцем компании
    if request.user.company != company:
        # Можно вернуть ошибку или перенаправить, если текущий пользователь не является владельцем компании
        return redirect('home')  # Пример перенаправления на главную страницу

    # Получаем все заказы для данной компании
    orders = Order.objects.filter(company=company)

    return render(request, 'main/see_orders.html', {'company': company, 'orders': orders})


#Создание новой компании
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/addcompany.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление компани")
        return dict(list(context.items()) + list(c_def.items()))

# def login(request):
#     return HttpResponse("авторизация")
# class ShowPost(DataMixin, DetailView):
#     model = companies
#     template_name = 'main/companyviews.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['post'])
#         return dict(list(context.items()) + list(c_def.items()))
#
# class CompaniesByCategoryView(ListView):
#     model = companies
#     template_name = 'companies_by_category.html'
#     context_object_name = 'companies'
#
#     def get_queryset(self):
#         category_slug = self.kwargs['category_slug']
#         category = Category.objects.get(slug=category_slug)
#         return companies.objects.filter(cat=category, is_active=True)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
#         return context
#
# def companies_by_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     companies_list = companies.objects.filter(cat=category, is_active=True)
#     return render(request, 'companies_by_category.html', {'category': category, 'companies': companies_list})
# Регистрация нового пользовартеля
class RegisterUser(CreateView,DataMixin):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

#Авторизация пользователя на сайте
class LoginUser(LoginView,DataMixin):

    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
    #разавторизация пользователя
    def logout_user(request):
        logout(request)
        return redirect('login')

