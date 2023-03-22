from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ArticleForm
from .models import Article

# Create your views here.

def article_search_view(request):
    #print(dir(request.GET))
    #print(request.GET)

    #query_dict = dict(request.GET)
    #query = query_dict.get('q')
    query = request.GET.get('q') 
    # qs = Article.objects.all()
    if query is not None:
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        qs = Article.objects.filter(lookups)
        # qs = Article.objects.search(query)

    context = {
        'object_list': qs
    }
    return render(request, 'articles/search.html', context=context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None) # if post then initial with post data else pretend its get requst
    context = {
        'form': form
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        return redirect(article_object.get_absolute_url()) # or below. but this is recommended. Django use this way
        #return redirect('article-detail', slug=article_object.slug)
    
        # title = form.cleaned_data.get('title')
        # content = form.cleaned_data.get('content')
        # # print(title, content)
        # article_object = Article.objects.create(title=title, content=content)
        # context['object'] = article_object
        # context['created'] = True
    return render(request, 'articles/create.html', context=context)

# def article_create_view(request):
#     form = ArticleForm()
#     # print(dir(form))
#     context = {
#         'form': form
#     }

#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         context['form'] = form
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             content = form.cleaned_data.get('content')
#             # print(title, content)
#             article_object = Article.objects.create(title=title, content=content)
#             context['object'] = article_object
#             context['created'] = True
#     return render(request, 'articles/create.html', context=context)

def article_details_view(request, slug=None):
    print(slug)

    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404

    context = {
        'object': article_obj
    }
    return render(request, 'articles/detail.html', context)