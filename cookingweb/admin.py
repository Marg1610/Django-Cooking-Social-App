from django.contrib import admin
from .models import Recipe, Tag, TagType, Rating
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(TagType)
admin.site.register(Rating)
