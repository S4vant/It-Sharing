from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
from django.views.generic import DetailView, DeleteView, UpdateView


# Create your views here.
def news_home(request):
    news = Article.objects.order_by('date')
    return render(request,'news/news_home.html', {"news": news})

class NewsDetailView(DetailView):
    model = Article
    template_name = 'news/detail_view.html'
    form_class = ArticleForm


class UpdateNewsView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/update.html'


class DeleteNewsView(DeleteView):
    model = Article
    success_url = '/news/'
    template_name = 'news/delete.html'



def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма неверна'

    form = ArticleForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request,'news/create.html', data)




