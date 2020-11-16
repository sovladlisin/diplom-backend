from django.contrib import admin
from django.db import models
from backend.models import Resource, Author, Class, File


class ResourceAdmin(admin.ModelAdmin):
    model = Resource


class AuthorAdmin(admin.ModelAdmin):
    model = Author


class ClassAdmin(admin.ModelAdmin):
    model = Class


class FileAdmin(admin.ModelAdmin):
    model = File


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(File, FileAdmin)
