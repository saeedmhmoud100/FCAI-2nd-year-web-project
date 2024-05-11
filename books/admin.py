from django.contrib import admin

from books.models import Book, BookImage, Viewers


# Register your models here.


class BookImageInline(admin.TabularInline):
    model = BookImage
    fields = ('image', 'slug', 'order', 'id')
    readonly_fields = ('slug', 'id')


class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline]


admin.site.register(Book, BookAdmin)

admin.site.register(Viewers)
