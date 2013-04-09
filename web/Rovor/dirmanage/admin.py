from django.contrib import admin

from dirmanage.models import Filesystem


class FilesystemAdmin(admin.ModelAdmin):
    fields = ( 'name', 'path')
    list_display = ('name','path')
    list_editable = ('path',)
    search_fields = ('name','path')
    ordering = ['name']

admin.site.register(Filesystem,FilesystemAdmin)


