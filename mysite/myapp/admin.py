from django.contrib import admin

from .models import Sentiment


# Register your models here.
@admin.register(Sentiment)
class SentimentModel(admin.ModelAdmin):
    # list_filter = ('id', 'text', 'label')
    list_display = ('text', 'label')
    search_fields = ['id', 'text', 'label']
    ordering = ['-id']