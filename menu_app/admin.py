from django.contrib import admin
from .models import Categories,Items,Lodge,Owner_Utility,CustomUser
# Register your models here.




admin.site.register(Categories)
admin.site.register(Items)
admin.site.register(Lodge)
admin.site.register(Owner_Utility)
admin.site.register(CustomUser)
