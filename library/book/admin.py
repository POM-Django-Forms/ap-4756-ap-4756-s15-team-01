from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'count', 'get_authors')
    list_filter = ('id', 'name', 'authors')
    ordering = ('id',)

    fieldsets = (
        ('Book Details', {
            'fields': ('name', 'description')
        }),
        ('Availability', {
            'fields': ('count',)
        }),
    )

    def get_authors(self, obj):
        return ", ".join([f"{a.name} {a.surname}" for a in obj.authors.all()])
    get_authors.short_description = 'Authors'