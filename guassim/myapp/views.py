from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Collection, Photo
from django.conf import settings
from django.utils import translation
from django.shortcuts import redirect
from django.urls.exceptions import Resolver404
# Create your views here.
def app_index(request): 
    # products = Product.objects.prefetch_related("product_image").filter(is_active = True)
    collections = Collection.objects.all()
    # Last 7 photos 
    photos = Photo.objects.all().order_by('-uploaded_at')[:7]
    
    return render(request, 'app/index.html',  {'collections': collections, 'photos': photos})

def page_about(request): 
    return render(request, 'app/about.html')
def page_contact(request):
    return render(request, 'app/contact.html')
def collection_detail(request, slug = None): 
    photos = Photo.objects.filter(collection__slug = slug)   
    # Get collections by id 
    collection = Collection.objects.filter(slug = slug) 
    if photos.count() == 0:
        return redirect('myapp:app_index')
    return render(request, 'app/collection_detail.html',  {'photos': photos,'collection': collection[0]})

def category_detail(request, slug = None): 
    category = get_object_or_404(Category, slug=slug)   
    collections = Collection.objects.filter(category__in = Category.objects.get(slug = slug).get_descendants(include_self=True))
   
    return render(request, 'app/category.html', {'category': category, 'collections': collections})
  

 