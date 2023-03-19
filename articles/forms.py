from django import forms
from .models import Article

# based on Model Form
class ArticleForm(forms.ModelForm):
    class Meta:
       model = Article
       fields = ['title', 'content']
       
    def clean(self):
       data = self.cleaned_data
       title = data.get('title')
       qs = Article.objects.filter(title__icontains=title)
       if qs.exists:
           self.add_error('title',f'"{title}" already exists')
       return data

# based on Form class
class ArticleFormOld(forms.Form):
    title  = forms.CharField()
    content  = forms.CharField()

    # def clean_title(self): # clean only title
    #     cleaned_data = self.cleaned_data # dictionary
    #     # print("cleaned_data", cleaned_data)
    #     title = cleaned_data.get('title')
    #     if title.lower().strip() == 'test':
    #         raise forms.ValidationError('This title is not allowed')
    #     # print("title", title)
    #     return title
    
    def clean(self): # clean everything
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title.lower().strip() == 'test':
            self.add_error('title','This title is taken. (Field error for title)') # this will show field error
        
        if len(title) <= 10:
            self.add_error('title','Title should be at least 10 characters (Field Error for title)')

        if 'test' in content or 'test' in title.lower():
            self.add_error('content','test cannot be in content (Field error for content)')
            raise forms.ValidationError('test is not allowed (None Field error)') # this will show nonfield error and is for all form

        return cleaned_data
    