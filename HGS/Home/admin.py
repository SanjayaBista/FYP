from django.contrib import admin
from .models import Category, Product, Comment , Contact, Size, ProductAttribute, Wishlist, ExchangeRate
from mptt.admin import DraggableMPTTAdmin

# Register your models here.

# class AdminCategory(admin.ModelAdmin):
#     list_display = ['name','slug', 'parent']
#     list_filter = ['name']

@admin.register(Category)
class AdminCategory2(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','slug','price','availibility','created','updated','category']
    list_filter = ['created','availibility','updated']
    list_editable = ['price','availibility']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Size)
class AdminSize(admin.ModelAdmin):
    list_display = ['title']

@admin.register(ProductAttribute)
class AdminAttribute(admin.ModelAdmin):
    list_display = ['product','size']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user','title','review','rating','created','updated']

    
@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['firstName', 'email', 'phoneNumber','message']

@admin.register(Wishlist)
class AdminWishlist(admin.ModelAdmin):
    list_display = ['user', 'product']

@admin.register(ExchangeRate)
class AdminExhangeRate(admin.ModelAdmin):
    list_display = ['currency', 'value']