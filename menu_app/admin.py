from django.contrib import admin
from .models import Categories,Items,Lodge,Owner_Utility,CustomUser
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Categories)
class Categories_UtilityAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'category_img')

@admin.register(CustomUser)
class CustomUser_UtilityAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_verified', 'is_chef', 'otp','username')




@admin.register(Items)
class Items_UtilityAdmin(admin.ModelAdmin):
    list_display = ('category', 'itemName', 'itemPrice','item_image','created_at', 'updated_at')

class Owner_UtilityAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'qr_code','delete_button')
    # delete_confirmation_template = 'owner_utiliti_delete.html'

    # def delete_button(self, obj):
    #     return '<a href="{}">Delete</a>'.format(
    #         reverse('admin_utiliti', args=[obj.pk])
    #     )
    # delete_button.short_description = 'Delete'

    def delete_button(self, obj):
        if obj.pk:
            url = reverse('admin_utiliti', args=[obj.pk])
            button_html = '<a href="{}">Delete</a>'.format(url)
            return format_html(button_html)
        else:
            return 'No PK available'

    delete_button.short_description = 'Delete'




admin.site.register(Owner_Utility,Owner_UtilityAdmin)