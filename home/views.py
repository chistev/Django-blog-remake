from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from home.models import Article

def index(request):
    articles_list = Article.objects.filter(is_published=True)
    # You create a paginator with all articles
    paginator = Paginator(articles_list, 6) # Splits into pages of 6
    
    page = request.GET.get('page')
    
    try:
        # Then you ask for a specific page
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
         # If page is out of range, deliver last page of results
        articles = paginator.page(paginator.num_pages)
    
    return render(request, 'home/index.html', {'articles':articles})

def article_detail(request):
    return render(request, 'home/article_detail.html')

def category_detail(request, slug):
    return render(request, 'home/related.html')
