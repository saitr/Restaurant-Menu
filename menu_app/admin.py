from django.contrib import admin
from .models import Categories,Items,Lodge,Owner_Utility,CustomUser,Order,SubOrder
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Categories)
class Categories_UtilityAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'category_img')


    def save_model(self, request, obj, form, change):
        # Check if the field values are repetitive
        if Categories.objects.filter(categoryName=obj.categoryName).exists():
            # Display an error message and prevent saving the object
            self.message_user(request, "Field value is already repetitive.", level='ERROR')
        else:
            # Save the object
            super().save_model(request, obj, form, change)


@admin.register(CustomUser)
class CustomUser_UtilityAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_verified', 'is_chef', 'otp','username')


@admin.register(Order)
class Order_UtilityAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'created_at', 'total_price','generate_bill')


@admin.register(SubOrder)
class SubOrder_UtilityAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'created_at', 'total_price','order_deliverd','order_place','main_orderid')



@admin.register(Items)
class Items_UtilityAdmin(admin.ModelAdmin):
    list_display = ('category', 'itemName', 'itemPrice','item_image','created_at', 'updated_at')


    def save_model(self, request, obj, form, change):
        # Check if the field values are repetitive
        if Items.objects.filter(itemName=obj.itemName).exists():
            # Display an error message and prevent saving the object
            self.message_user(request, "Field value is already repetitive.", level='ERROR')
        else:
            # Save the object
            super().save_model(request, obj, form, change)


class Owner_UtilityAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'qr_code','delete_button')

    def save_model(self, request, obj, form, change):
        # Check if the field values are repetitive
        if Owner_Utility.objects.filter(table_number=obj.table_number).exists():
            # Display an error message and prevent saving the object
            self.message_user(request, "Field value is already repetitive.", level='ERROR')
        else:
            # Save the object
            super().save_model(request, obj, form, change)


    def delete_button(self, obj):

        if obj.pk:
            url = reverse('admin_utiliti', args=[obj.pk])
            button_html = '<a href="{}">Delete</a>'.format(url)
            return format_html(button_html)
        else:
            return 'No PK available'

    delete_button.short_description = 'Delete'




admin.site.register(Owner_Utility,Owner_UtilityAdmin)