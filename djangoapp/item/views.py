from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Item, Category
from django.db.models import Q
# Create your views here.

def browse (request):
    query= request.GET.get('query', '')
    category_id= request.GET.get('category', 0)
    categories= Category.objects.all()

    browse = Item.objects.filter(is_sold=False)

    if category_id:
        browse= browse.filter(category_id=category_id)

    if query:
        browse= browse.filter(Q(name__icontains= query) | Q(description__icontains= query))
    
    return render(request, 'item/browse.html', {
        'browse': browse,
        'query': query,
        'categories':categories,
        'category_id': int(category_id)
    })

def detail (request, pk):
    item = get_object_or_404(Item, pk=pk)                                                   #yields the 404 error if the object is not found in database
    relatd_items= Item.objects.filter(category= item.category, is_sold= False).exclude(pk=pk)[0:3]   #to show related items
    return render(request, 'item/detail.html', {
        'item':item,
        'related_items': relatd_items
    })

# to call/access this method, only if, django make login required by using decorator @login_required
# if you try to access this without being authenticated, django will redirect to the login page
@login_required
def new(request):
    if request.method == "POST":
        form=NewItemForm(request.POST, request.FILES)

        if form.is_valid():       
            '''cannot save into database created by this form field.with commit=False, then it will return an object that hasn’t yet been saved to the database. In this case, it is up to you to call save() on the resulting model instance.READ here https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/'''
            item= form.save(commit=False)
            item.created_by= request.user
            item.save()

            return redirect('item:detail', pk=item.id)      #id of just created item object
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def edit(request, pk):
    item= get_object_or_404(Item, pk=pk, created_by= request.user)

    if request.method == "POST":
        form= EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():       
            form.save()         #since the created by, is already set

            return redirect('item:detail', pk=item.id)      #id of just created item object
    else:
        form = EditItemForm(instance= item)     #this form was empty hence will give error, so instance=item is passed on

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def delete(request, pk):
    item= get_object_or_404(Item, pk=pk, created_by= request.user)  #can't delete the object if you're not creator
    item.delete()

    return redirect('dashboard:index')

