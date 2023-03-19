from django.contrib import admin
from django.utils.html import mark_safe
from E_Shop_API.E_Shop_Products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Custom product field in admin panel """
    list_display = ('get_photo', 'name', 'count', 'price', 'updated_at', 'active')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_editable = ('active',)
    list_filter = ('description', 'price')
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    save_on_top = True

    list_per_page = 20

    def get_photo(self, obj):
        """ Method which return img in admin panel """
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        else:
            return '-'

    get_photo.short_description = 'Photo'
