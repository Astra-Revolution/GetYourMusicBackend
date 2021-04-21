from django.contrib import admin

# Register your models here.

from .models import Publication, Comment, Following, Notification, Genre, Instrument

admin.site.register(Publication)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Notification)
admin.site.register(Genre)
admin.site.register(Instrument)
