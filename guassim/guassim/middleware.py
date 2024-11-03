from django.utils import translation
from django.conf import settings
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.urls.exceptions import Resolver404

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for admin and non-translated URLs
        if request.path.startswith('/admin/') or request.path.startswith('/change-language/'):
            return self.get_response(request)
        
        # if request.path includes "images", remove language prefix
        if request.path.startswith('/images/'): 
            return self.get_response(request)
     
        # Get language from cookie
        # language_from_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        
        # if language_from_cookie:
        #     # Check if URL already has language prefix
        #     has_prefix = any(request.path.startswith(f'/{code}/') 
        #                    for code, _ in settings.LANGUAGES) 
        #     if not has_prefix and language_from_cookie in [lang[0] for lang in settings.LANGUAGES]:
        #         # Redirect to URL with language prefix
        #         current_path = request.path_info
        #         if current_path.startswith('/'):
        #             current_path = current_path[1:]
        #         new_url = f'/{language_from_cookie}/{current_path}'
                
        #         return redirect(new_url)

        response = self.get_response(request)
        return response