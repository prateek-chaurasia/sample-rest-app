from django.contrib import admin
from .models import Snippet
# Register your models here.

class SnippetAdmin(admin.ModelAdmin):
	list_display = ('owner','title', 'code', 'linenos','language','style')

admin.site.register(Snippet, SnippetAdmin)
