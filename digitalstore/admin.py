from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(BrandProduct)
admin.site.register(FavouriteProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Profile)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'get_icon_admin']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm

    def get_icon_admin(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30" />')
            except:
                return '-'
        else:
            return '-'

    get_icon_admin.short_description = 'Иконка'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'category', 'quantity', 'color_name', 'created_at', 'get_img_admin')
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'quantity', 'category']

    def get_img_admin(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="50" />')
            except:
                return '-'
        else:
            return '-'
