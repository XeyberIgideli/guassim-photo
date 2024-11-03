from django.contrib import admin
from .models import (Category, Collection, Photo,SiteSetting, About, Favorites)
from mptt.admin import MPTTModelAdmin
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage 
from modeltranslation.admin import TranslationAdmin
# Register your models here.

@admin.register(Favorites)
class AdminFavorites(admin.ModelAdmin):
    list_display = ('name', 'phone','message','image_tag','message_reason',)
    readonly_fields = ('name', 'phone','message','collection','photo','message_reason','image_tag',)
    exclude = ('reason',)
    def has_add_permission(self, request):
        return False
    
@admin.register(Category)
class AdminCategory (TranslationAdmin, MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # it will prepopulate the slug field based on the name field
    
class CollectionPhotoInline (admin.TabularInline):
    model = Photo

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'share_to_customer', 'uploaded_at', 'category','enable_folder_download')
    exclude = ('google_drive_folder_download_link','share_to_customer')
    # list_filter = ('category', 'enable_folder_download')
    search_fields = ('title', 'description')
    inlines = [CollectionPhotoInline]
    def delete_model(self, request, obj): 
        if obj.image:
            if default_storage.exists(obj.image.name):
                default_storage.delete(obj.image.name)
         
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)  # Call the delete_model() method when the queryset is deleted  
        super().delete_queryset(request, queryset)  #  

admin.site.register(Collection, CollectionAdmin)

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active"]
    search_fields = ["title"]

    def has_add_permission(self, request):
        # Prevent adding SiteSetting if it already exists
        if SiteSetting.objects.exists():
            return False
        return True

    
admin.site.register(SiteSetting, SiteSettingAdmin) 

@admin.register(About)
class AboutAdmin(TranslationAdmin):
    list_display = ["name", ]
    search_fields = ["name"]

    def has_add_permission(self, request):
        # Prevent adding About if it already exists
        if About.objects.exists():
            return False
        return True 
    