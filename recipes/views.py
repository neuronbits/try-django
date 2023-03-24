from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient

# Create your views here.

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    print(qs)
    context = {
        'object_list': qs
    }
    return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    context = {
        'object': obj
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'recipes/create-update.html', context)


@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    RecipeIngredientFormset = modelformset_factory(RecipeIngredient,form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all()
    formset = RecipeIngredientFormset (request.POST or None, queryset=qs)

    #form_2 = RecipeIngredientForm(request.POST or None)
    #Formset = modelformset_factory(Model, form=ModelForm, extra=0)

    context = {
        'form': form,
        #'form_2': form_2,
        'formset': formset,
        'object': obj
    }
    #if all([form.is_valid(), form_2.is_valid()]):
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            if child.recipe is None:
                child.recipe = parent
            child.save ()

        # child = form_2.save(commit=False)
        # child.recipe = parent # recipe is foreign key
        # child.save()

        context ['message'] = 'Data saved.'
    return render(request, 'recipes/create-update.html', context)
