
from django.shortcuts import redirect
from django.utils import translation
from django.urls import resolve, reverse
from django.conf import settings
from django.urls.exceptions import Resolver404

def change_language(request):
    lang_code = request.GET.get('language')
    if lang_code and lang_code in [lang[0] for lang in settings.LANGUAGES]:
        # Store the current path
        next_path = request.META.get('HTTP_REFERER', '/')
        
        try:
            # Remove the old language prefix if it exists
            resolved = resolve(next_path)
            if resolved.namespace == 'i18n_patterns':
                current_lang = translation.get_language()
                next_path = next_path.replace(f'/{current_lang}/', '/', 1)
        except Resolver404:
            next_path = '/'

        # Ensure the path starts with a slash
        if not next_path.startswith('/'):
            next_path = '/' + next_path

        # Create the new URL with language prefix
        new_url = f'/{lang_code}{next_path}'
        
        # Create response with the new URL
        response = redirect(new_url)
        
        # Set language cookie
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, 
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path='/'
        )
        
        return response
    
    return redirect('/')