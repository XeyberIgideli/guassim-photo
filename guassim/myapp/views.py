import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Collection, Photo, Favorites
from django.conf import settings
from django.utils import translation
from django.shortcuts import redirect
from django.urls.exceptions import Resolver404
from django.http import JsonResponse
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
    collection = Collection.objects.filter(slug = slug) 
    disk_download = request.GET.get('share')    
    if disk_download and not collection[0].share_to_customer.endswith(disk_download):
        disk_download = False
    else:
        if photos.count() == 0:
          return redirect('myapp:app_index')
        return render(request, 'app/collection_detail.html',  {'photos': photos,'collection': collection[0], 'share_disk': disk_download})
    
def category_detail(request, slug = None): 
    category = get_object_or_404(Category, slug=slug)   
    collections = Collection.objects.filter(category__in = Category.objects.get(slug = slug).get_descendants(include_self=True))
   
    return render(request, 'app/category.html', {'category': category, 'collections': collections})

def photo_detail(request, pk = None): 
    photo = Photo.objects.filter(pk = pk) 
    # if photo not exists, redirect to homepage  
    if photo.exists() == False:
        return redirect('myapp:app_index')
    return render(request, 'app/single_photo.html', {'photo': photo[0]}) 
  

def create_favorite (request):
    if request.method == "POST":
        name = request.POST.get('name')  
        phone = request.POST.get('phone')  
        message = request.POST.get('message')
        collection_id = request.POST.get('collectionId')  
        photoId = request.POST.get('photoId')
        reasonInput = request.POST.get('reason')
        # check fields
        if not name or not phone or not collection_id:
            # return error for displaying in template
            return JsonResponse({'success': False}, status=400) 
         
        # create new favorite
        new_favorite = Favorites.objects.create(
            name = name,
            phone = phone,
            message = message,
            collection_id = collection_id,  
            photo_id = photoId,
            reason = reasonInput
        ) 
        
        print(request.POST) 
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

 