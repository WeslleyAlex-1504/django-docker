from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from .forms import LoteEstoqueForm, ProdutoForm
from .models import LoteEstoque, Produto


class DashboardView(TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.localdate()

        produtos = Produto.objects.prefetch_related('lotes')
        lotes = LoteEstoque.objects.select_related('produto')

        context.update({
            'produtos': produtos,
            'lotes_vencidos': lotes.filter(data_vencimento__lt=hoje),
            'lotes_a_vencer': lotes.filter(data_vencimento__gte=hoje, data_vencimento__lte=hoje + timedelta(days=30)),
            'total_itens': lotes.aggregate(total=Sum('quantidade')).get('total') or 0,
        })
        return context


class ProdutoCreateView(CreateView):
    form_class = ProdutoForm
    template_name = 'inventory/form.html'

    def get_success_url(self):
        return self.request.GET.get('next') or '/'


class LoteCreateView(CreateView):
    form_class = LoteEstoqueForm
    template_name = 'inventory/form.html'

    def get_success_url(self):
        return self.request.GET.get('next') or '/'


def home_redirect(request):
    return redirect('inventory:dashboard')
