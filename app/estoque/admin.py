from django.contrib import admin

from .models import Fruta


@admin.register(Fruta)
class FrutaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'data_validade', 'quantidade_estoque', 'status', 'created_at')
    list_filter = ('tipo', 'status')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')
