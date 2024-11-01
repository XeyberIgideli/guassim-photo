from modeltranslation.translator import translator, TranslationOptions
from .models import About, Category

class AboutTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'text1', 'text2', 'section1', 'section2', 'section3')
    
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    
translator.register(About, AboutTranslationOptions)    
translator.register(Category, CategoryTranslationOptions)    