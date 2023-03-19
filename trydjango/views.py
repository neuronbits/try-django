import random
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from articles.models import Article


def home_view(request, *args, **kwargs):
    name = 'Mr John'
    number = random.randint(1,2)
    article_object = Article.objects.get(id=number)
    article_list = Article.objects.all()
    print(args, kwargs)
    
    context = {
        'article_list': article_list, 
        'id': article_object.id,
        'title': article_object.title,
        'content': article_object.content,
    }
    tmpl = get_template('home-view.html')
    tmpl_string = tmpl.render(context=context)
    # tmpl_string2 = tmpl.render(context=context2)
    # tmpl_string3 = tmpl.render(context=context3)

    HTML_STRING = render_to_string('home-view.html',context=context)
    # HTML_STRING = f"""
    # <h1>{article_object.title} - {article_object.id}</h1>
    # <p>{article_object.content}</p>
    # """

    return HttpResponse(HTML_STRING)
