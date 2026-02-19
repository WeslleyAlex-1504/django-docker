from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Produto, LoteEstoque


class LoteInline(admin.TabularInline):
    model = LoteEstoque
    extra = 0
    fields = ('codigo_lote', 'quantidade', 'data_vencimento')
    readonly_fields = ('vencido',)
    show_change_link = True

    def vencido(self, obj):
        if obj.vencido:
            return format_html('<span style="color: #dc2626; font-weight: bold;">⚠️ VENCIDO</span>')
        return format_html('<span style="color: #16a34a;">✓ Válido</span>')
    vencido.short_description = 'Status'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sku', 'get_status_badge', 'quantidade_total', 'criado_em', 'get_actions')
    list_display_links = ('nome', 'sku')
    search_fields = ('nome', 'sku', 'descricao')
    list_filter = ('ativo', 'criado_em')
    list_per_page = 25
    ordering = ('-criado_em',)
    inlines = [LoteInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'sku', 'descricao'),
            'classes': ('wide',),
        }),
        ('Configurações', {
            'fields': ('ativo',),
            'classes': ('collapse',),
        }),
    )

    def get_status_badge(self, obj):
        if obj.ativo:
            return format_html('<span style="background: #dcfce7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">ATIVO</span>')
        return format_html('<span style="background: #fee2e2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">INATIVO</span>')
    get_status_badge.short_description = 'Status'

    def get_actions(self, obj):
        return format_html(
            '<a href="{}" style="color: #10b981; margin-right: 1rem;">✏️ Editar</a>'
            '<a href="{}" style="color: #dc2626;">🗑️ Excluir</a>',
            reverse('admin:inventory_produto_change', args=[obj.pk]),
            reverse('admin:inventory_produto_delete', args=[obj.pk])
        )
    get_actions.short_description = 'Ações'


@admin.register(LoteEstoque)
class LoteEstoqueAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'produto', 'quantidade', 'data_vencimento', 'get_status_badge', 'get_days_until_expiry', 'get_actions')
    list_display_links = ('codigo_lote',)
    search_fields = ('codigo_lote', 'produto__nome', 'produto__sku')
    list_filter = ('data_vencimento', 'produto__ativo')
    list_per_page = 25
    ordering = ('data_vencimento',)
    date_hierarchy = 'data_vencimento'

    fieldsets = (
        ('Informações do Lote', {
            'fields': ('produto', 'codigo_lote', 'quantidade', 'data_vencimento'),
            'classes': ('wide',),
        }),
    )

    def get_status_badge(self, obj):
        if obj.vencido:
            return format_html('<span style="background: #fee2e2; color: #dc2626; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">VENCIDO</span>')
        elif obj.data_vencimento <= obj.data_vencimento.today() + obj.data_vencimento.timedelta(days=30):
            return format_html('<span style="background: #fef3c7; color: #d97706; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">PRÓXIMO</span>')
        return format_html('<span style="background: #dcfce7; color: #166534; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">VÁLIDO</span>')
    get_status_badge.short_description = 'Status'

    def get_days_until_expiry(self, obj):
        from django.utils import timezone
        today = timezone.localdate()
        days = (obj.data_vencimento - today).days

        if days < 0:
            return format_html('<span style="color: #dc2626; font-weight: bold;">{} dias</span>', abs(days))
        elif days <= 30:
            return format_html('<span style="color: #d97706; font-weight: bold;">{} dias</span>', days)
        return format_html('<span style="color: #16a34a;">{} dias</span>', days)
    get_days_until_expiry.short_description = 'Dias p/ Vencer'

    def get_actions(self, obj):
        return format_html(
            '<a href="{}" style="color: #10b981; margin-right: 1rem;">✏️ Editar</a>'
            '<a href="{}" style="color: #dc2626;">🗑️ Excluir</a>',
            reverse('admin:inventory_loteestoque_change', args=[obj.pk]),
            reverse('admin:inventory_loteestoque_delete', args=[obj.pk])
        )
    get_actions.short_description = 'Ações'
    list_filter = ('data_vencimento', 'produto')
    search_fields = ('produto__nome', 'codigo_lote')
