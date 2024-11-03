from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _ # type: ignore
from django.core.files.storage import default_storage 
from google.oauth2 import service_account
from googleapiclient.discovery import build 
from io import BytesIO
import zipfile
from googleapiclient.http import MediaIoBaseUpload
import io
import os
import json
import re
import uuid
from tinymce.models import HTMLField
from .utils import unique_image_path
from functools import partial
from django.utils.html import format_html

# Create your models here. 
class About(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = HTMLField() 
    section1 = models.CharField(max_length=255, verbose_name=_("Section 1"), null=True, blank=True) 
    section2 = models.CharField(max_length=255, verbose_name=_("Section 2"), null=True, blank=True)
    section3 = models.CharField(max_length=255, verbose_name=_("Section 3"), null=True, blank=True)  
    text1 = HTMLField() 
    text2 = HTMLField() 
    image = models.ImageField(upload_to=partial(unique_image_path, folder_name="about"), verbose_name=_("Profile Photo"), null=True, blank=True) 

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"
        
    def save (self, *args, **kwargs):
            old_instance = About.objects.get(pk=self.pk) 
            # Handle image deletion
            if old_instance.image != self.image:  
                if old_instance.image: 
                    if default_storage.exists(old_instance.image.name):
                        default_storage.delete(old_instance.image.name)   

            super().save(*args, **kwargs) 
            
    def delete(self, *args, **kwargs): 
        if self.image: 
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
 
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.name

class SiteSetting(models.Model):
    title = models.CharField(max_length=255, verbose_name="Site title")
    description = models.TextField(verbose_name="Site description")
    keywords = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="site_logos/", verbose_name="Logo", null=True, blank=True)
    favicon = models.ImageField(upload_to="favicons/", verbose_name="Favicon", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    whatsapp_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)  
    instagram_url = models.URLField(null=True, blank=True) 
    behance_url = models.URLField(null=True, blank=True)  
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.title
    
class Category (MPTTModel): 
    name = models.CharField(
        verbose_name= "Category Name",
        help_text= "Required and unique",
        max_length= 255,
        unique = True
    )
    slug = models.SlugField(verbose_name= "Category slug", max_length=255, unique= True,blank=True)
    parent = TreeForeignKey("self", on_delete= models.CASCADE, null = True, blank = True)
    is_active = models.BooleanField(default= True)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = _("Category")    
        verbose_name_plural = _("Categories")    
       
    def get_absolute_url(self): 
        return reverse("myapp:category_detail", args=[self.slug])   
    def __str__(self):
        return self.name  
      
    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
    


class Collection(models.Model):
    title = models.CharField(max_length=100) 
    image = models.ImageField(verbose_name=_("Image"),upload_to=partial(unique_image_path, folder_name="collections"), help_text=_("Please add image"), max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    slug = models.SlugField(verbose_name="Collection slug", max_length=255, unique=True, null=True, blank=True)
    google_drive_folder_link = models.CharField(max_length=250, null=True, blank=True)  
    enable_folder_download = models.BooleanField(default=False, verbose_name="Enable folder download")
    google_drive_folder_download_link = models.URLField(null=True, blank=True)
    share_to_customer = models.URLField(null=True, blank=True)
    def save(self, *args, **kwargs): 
        is_new = self.pk is None
        should_process_drive = False
        
        # Check if this is a new instance with a drive link
        if is_new and self.google_drive_folder_link:
            should_process_drive = True
            
        # For existing instances, check if drive link changed
        elif not is_new:
            old_instance = Collection.objects.get(pk=self.pk)
            # Handle image deletion
            if old_instance.image != self.image:  
                if old_instance.image: 
                    if default_storage.exists(old_instance.image.name):
                        default_storage.delete(old_instance.image.name)
            
            # Check if drive link changed
            if old_instance.google_drive_folder_link != self.google_drive_folder_link:
                should_process_drive = True
                # Delete existing photos if drive link changed
                self.photos.all().delete() 
        # Generate slug and save
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        # Process Google Drive photos only if needed
        if should_process_drive and self.google_drive_folder_link:
            self.add_photos_from_drive(self.google_drive_folder_link, self.enable_folder_download)
                  
    def extract_folder_id(self, url):
        match = re.search(r'/folders/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
        return None
    def extract_file_id(self, url):
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
        return None    
    def add_photos_from_drive(self, google_drive_folder_link, enableFolderDownload):
        folder_id = self.extract_folder_id(google_drive_folder_link) 
        if not folder_id:
            return
            
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(os.getenv('GOOGLE_CREDENTIALS')),
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=credentials)
          
        results = service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/'",
            fields="files(id, name, webViewLink)"
        ).execute()
        
        items = results.get('files', [])
        
        if enableFolderDownload:
            # Create ZIP file in memory
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file in results.get('files', []):
                    request = service.files().get_media(fileId=file['id'])
                    file_content = request.execute()
                    zip_file.writestr(file['name'], file_content)
            
            zip_buffer.seek(0)
            
            # Upload the ZIP file to Drive
            zip_metadata = {
                'name': f'{self.title}_archive.zip',
                'mimeType': 'application/zip'
            }
            
            media = MediaIoBaseUpload(zip_buffer, mimetype='application/zip', resumable=True)
            zip_file = service.files().create(
                body=zip_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            # Make the ZIP file publicly accessible
            service.permissions().create(
                fileId=zip_file['id'],
                body={
                    'type': 'anyone',
                    'role': 'reader'
                }
            ).execute()
            
            # Generate direct download link for the ZIP
            download_link = f"https://drive.google.com/uc?export=download&id={zip_file['id']}"
            self.share_to_customer = settings.SITE_LINK + f'/collection/{self.slug}?share={uuid.uuid4()}'
            self.google_drive_folder_download_link = download_link
            self.save()    
        # Create photos using self.id
        for item in items: 
            Photo.objects.create(
                collection=self,  # Use the instance directly instead of just the ID
                url="https://lh3.googleusercontent.com/d/" + self.extract_file_id(item['webViewLink']),
                google_drive_photo_id = self.extract_file_id(item['webViewLink'])
            )
            
    def delete(self, *args, **kwargs): 
        if self.image: 
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
 
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class Photo(models.Model): 
    url = models.URLField() 
    alt_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='photos')   
    google_drive_photo_id = models.CharField(max_length=250, null=True, blank=True)
    class Meta:
        verbose_name = _("Collection Photo")
        verbose_name_plural = _("Collection Photos")
        
    def __str__(self):
        return self.url
    
class Favorites(models.Model):
    name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    message = models.TextField(blank=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='favorites', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photos', null=True)
    reason = models.CharField(max_length=250, blank=False,null=True)
    class Meta:
        verbose_name = _("Favorites")
        verbose_name_plural = _("Favorites")
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def message_reason (self):
        if self.reason:
            return format_html(f'<span style="color: #ffc107;">{self.reason}</span>')
        return "No Reason"
        
    def image_tag(self):
        if self.photo and hasattr(self.photo, 'url'):  
            return format_html(f'<img src="{self.photo.url}"  height="300" />')
        return "No Image"  
    def __str__(self):
        return self.name
    
 
     
   