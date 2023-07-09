from django.shortcuts import render, redirect
from item.models import Item, Category

from .forms import SignupForm

# Create your views here.
def index(request):
    items= Item.objects.filter(is_sold = False)[0:6]    #to show new six items, absolutely not sold
    categories= Category.objects.all()                  #to show all categories of the items
                   
    return render(request, 'core/index.html',{          #to use the items & categories in templates
        'items': items,
        'categories': categories,                     
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm (request.POST)

        if form.is_valid():
            form.save()                 #this will save into database
            return redirect('/login/')
    else:
        form = SignupForm
    
    return render(request, 'core/signup.html', {
        "form":form
    })
