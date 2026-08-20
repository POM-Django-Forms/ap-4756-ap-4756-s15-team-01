from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'patronymic', 'get_books')
    list_filter = ('id', 'name', 'surname')
    filter_horizontal = ('books',)
    ordering = ('id',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'surname', 'patronymic')
        }),
        ('Books', {
            'fields': ('books',)
        }),
    )

    def get_books(self, obj):
        return ", ".join([b.name for b in obj.books.all()])
    get_books.short_description = 'Books'