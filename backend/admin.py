from django.contrib import admin
from django.db import models
from backend.models import Resource, Author, Class, File, ResourceTexts


class ResourceAdmin(admin.ModelAdmin):
    model = Resource


class AuthorAdmin(admin.ModelAdmin):
    model = Author


class ClassAdmin(admin.ModelAdmin):
    model = Class


class FileAdmin(admin.ModelAdmin):
    model = File


class ResourceTextsAdmin(admin.ModelAdmin):
    model = ResourceTexts


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(ResourceTexts, ResourceTextsAdmin)
