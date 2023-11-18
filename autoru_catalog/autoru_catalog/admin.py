from django.contrib import admin

from autoru_catalog.models import Mark, Model


@admin.register(Mark)
class AssetAdmin(admin.ModelAdmin):
    pass


@admin.register(Model)
class AssetAdmin(admin.ModelAdmin):
    pass
