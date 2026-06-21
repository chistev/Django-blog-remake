from django.shortcuts import render
from home.models import Article

def index(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'home/index.html', {'articles':articles})

def article_detail(request):
    return render(request, 'home/article_detail.html')

def category_detail(request, slug):
    return render(request, 'home/related.html')
