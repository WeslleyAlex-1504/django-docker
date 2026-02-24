from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Produto, LoteEstoque


class LoteInline(admin.TabularInline):
    model = LoteEstoque
    extra = 0
    fields = ('codigo_lote', 'quantidade', 'data_vencimento', 'status_vencimento')
    readonly_fields = ('codigo_lote', 'status_vencimento')
    show_change_link = True

    def status_vencimento(self, obj):
        if obj.vencido:
            return format_html('<span style="color: #dc2626; font-weight: bold;">⚠️ VENCIDO</span>')
        elif obj.dias_para_vencer <= 0:
            return format_html('<span style="color: #ea580c; font-weight: bold;">🔴 VENCE HOJE</span>')
        elif obj.dias_para_vencer <= 7:
            return format_html('<span style="color: #ea580c; font-weight: bold;">🟠 VENCE EM BREVE</span>')
        elif obj.dias_para_vencer <= 30:
            return format_html('<span style="color: #d97706; font-weight: bold;">🟡 PRÓXIMO A VENCER</span>')
        return format_html('<span style="color: #16a34a;">✅ VÁLIDO</span>')
    status_vencimento.short_description = 'Status'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'get_status_badge', 'total_lotes', 'quantidade_total', 'criado_em')
    list_display_links = ('nome', 'sku')
    search_fields = ('nome', 'sku', 'descricao')
    list_filter = ('ativo', 'criado_em')
    list_per_page = 25
    ordering = ('-criado_em',)
    inlines = [LoteInline]
    date_hierarchy = 'criado_em'

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'sku', 'descricao'),
            'classes': ('wide',),
        }),
        ('Configurações', {
            'fields': ('ativo',),
            'classes': ('collapse',),
        }),
        ('Informações do Sistema', {
            'fields': ('criado_em',),
            'classes': ('collapse', 'wide'),
            'description': 'Dados automáticos do sistema'
        }),
    )

    readonly_fields = ('criado_em', 'sku')

    def get_status_badge(self, obj):
        if obj.ativo:
            return format_html('<span style="background: #dcfce7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">✅ ATIVO</span>')
        return format_html('<span style="background: #fee2e2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">❌ INATIVO</span>')
    get_status_badge.short_description = 'Status'

    def total_lotes(self, obj):
        return obj.total_lotes
    total_lotes.short_description = 'Lotes'


@admin.register(LoteEstoque)
class LoteEstoqueAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'get_produto', 'quantidade', 'data_vencimento', 'get_status_badge', 'get_days_until_expiry')
    list_display_links = ('codigo_lote',)
    search_fields = ('codigo_lote', 'produto__nome', 'produto__sku')
    list_filter = ('data_vencimento', 'produto__ativo', 'produto')
    list_per_page = 25
    ordering = ('data_vencimento',)
    date_hierarchy = 'data_vencimento'
    readonly_fields = ('codigo_lote', 'criado_em')

    fieldsets = (
        ('Informações do Lote', {
            'fields': ('produto', 'codigo_lote', 'quantidade', 'data_vencimento'),
            'classes': ('wide',),
        }),
        ('Informações do Sistema', {
            'fields': ('criado_em',),
            'classes': ('collapse', 'wide'),
            'description': 'Dados automáticos do sistema'
        }),
    )

    def get_produto(self, obj):
        return format_html('<strong>{}</strong> ({})', obj.produto.nome, obj.produto.sku)
    get_produto.short_description = 'Produto'

    def get_status_badge(self, obj):
        if obj.vencido:
            return format_html('<span style="background: #fee2e2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">⚠️ VENCIDO</span>')
        elif obj.dias_para_vencer <= 0:
            return format_html('<span style="background: #fed7aa; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">🔴 VENCE HOJE</span>')
        elif obj.dias_para_vencer <= 7:
            return format_html('<span style="background: #fed7aa; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">🟠 EM BREVE</span>')
        elif obj.dias_para_vencer <= 30:
            return format_html('<span style="background: #fef3c7; color: #b45309; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">🟡 PRÓXIMO</span>')
        return format_html('<span style="background: #dcfce7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">✅ VÁLIDO</span>')
    get_status_badge.short_description = 'Status'

    def get_days_until_expiry(self, obj):
        days = obj.dias_para_vencer

        if days < 0:
            return format_html('<span style="color: #dc2626; font-weight: bold;">-{} d</span>', abs(days))
        elif days == 0:
            return format_html('<span style="color: #ea580c; font-weight: bold;">HOJE</span>')
        elif days <= 7:
            return format_html('<span style="color: #ea580c; font-weight: bold;">{} d</span>', days)
        elif days <= 30:
            return format_html('<span style="color: #d97706; font-weight: bold;">{} d</span>', days)
        return format_html('<span style="color: #16a34a;">{} d</span>', days)
    get_days_until_expiry.short_description = 'Dias'
