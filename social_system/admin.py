from django.contrib import admin

# Register your models here.

from .models import Publication, Comment
admin.site.register(Publication)
admin.site.register(Comment)