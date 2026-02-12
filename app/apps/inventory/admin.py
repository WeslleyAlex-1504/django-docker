from django.contrib import admin
from .models import Produto, LoteEstoque


class LoteInline(admin.TabularInline):
    model = LoteEstoque
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'ativo', 'quantidade_total')
    search_fields = ('nome', 'sku')
    list_filter = ('ativo',)
    inlines = [LoteInline]


@admin.register(LoteEstoque)
class LoteEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'codigo_lote', 'quantidade', 'data_vencimento', 'vencido')
    list_filter = ('data_vencimento', 'produto')
    search_fields = ('produto__nome', 'codigo_lote')
