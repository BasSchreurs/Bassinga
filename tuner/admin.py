from django.contrib import admin
from .models import FretTab

@admin.register(FretTab)
class FretTabAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')  # show position
    list_editable = ('position',)        # make it editable in list view
    ordering = ('position',)             # default ordering in admin
