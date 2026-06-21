from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from home.models import Article
from django.db.models import Q

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

def search(request):
    query = request.GET.get('q', '') # query = '' when no parameter
    
    results = []
    results_count = 0
    
    if query:
        # This searches for articles where ANY condition is true
        # WITHOUT Q - AND condition (ALL must be true)
        results = Article.objects.filter(
            Q(title__icontains=query) | # OR
            Q(content__icontains=query) | # OR
            Q(category__name__icontains=query),
            is_published=True # ← AND condition
        ).distinct() # WITHOUT .distinct() An article that matches MULTIPLE conditions would appear as many times!
        
        results_count = results.count()
        
        paginator = Paginator(results, 6)
        page = request.GET.get('page')
        
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
    
    else:
        articles = []
        
    
    return render(request, 'home/search.html', {
        'articles':articles,
        'query':query,
        'results_count':results_count
    })
        
