from django.contrib import admin
from .models import *

# Register your models here


class ImagesTublerinline(admin.TabularInline):
    model = images
class TagTublerinline(admin.TabularInline):
    model = Tag
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline,TagTublerinline]

admin.site.register(Addresses)
admin.site.register(Categories)
admin.site.register(Products,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profiles)

admin.site.register(fabrics)
admin.site.register(Colors)
admin.site.register(Size)
admin.site.register(filter_price)
admin.site.register(images)
admin.site.register(Tag)