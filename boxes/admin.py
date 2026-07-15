from django.contrib import admin

from .models import Box


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'serial_no', 'name', 'internal_length', 'internal_width',
        'internal_height', 'max_weight_capacity', 'cost',
    )
    search_fields = ('serial_no', 'name')