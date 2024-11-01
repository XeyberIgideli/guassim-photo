from .models import Category, SiteSetting, About
# Create your views here.
 
def categories (request):
    return {
        'categories': Category.objects.filter(level=0)
    }
    
def site_settings (request):
    return {
        'site_settings': SiteSetting.objects.filter(is_active=True).first()
    } 
    
def about (request):
    return {
        'about': About.objects.filter().first()
}    
    
    