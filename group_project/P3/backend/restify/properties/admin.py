from django.contrib import admin

# Register your models here.
from .models import Property, Amenity, Pictures, Availability
admin.site.register(Property)
admin.site.register(Amenity)
admin.site.register(Availability)



class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
admin.site.register(Pictures, PictureAdmin)