from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_book', 'get_user', 'created_at', 'plated_end_at', 'end_at')
    list_filter = ('book__id', 'book__name', 'book__authors', 'created_at', 'plated_end_at')
    ordering = ('id',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Order Details', {
            'fields': ('book', 'user', 'created_at', 'plated_end_at')
        }),
        ('Return Status', {
            'fields': ('end_at',)
        }),
    )

    def get_book(self, obj):
        return obj.book.name
    get_book.short_description = 'Book'

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user.short_description = 'User'