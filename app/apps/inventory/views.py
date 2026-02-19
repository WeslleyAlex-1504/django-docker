from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import LoteEstoqueForm, ProdutoForm
from .models import LoteEstoque, Produto


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'
    login_url = '/accounts/login/'

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


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    form_class = ProdutoForm
    template_name = 'inventory/form.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        return self.request.GET.get('next') or '/estoque/'


class LoteCreateView(LoginRequiredMixin, CreateView):
    form_class = LoteEstoqueForm
    template_name = 'inventory/form.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        return self.request.GET.get('next') or '/estoque/'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('inventory:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class HomeView(TemplateView):
    template_name = 'home.html'


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'inventory/form.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return reverse_lazy('inventory:dashboard')


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'inventory/produto_confirm_delete.html'
    success_url = reverse_lazy('inventory:dashboard')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Produto excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class LoteUpdateView(LoginRequiredMixin, UpdateView):
    model = LoteEstoque
    form_class = LoteEstoqueForm
    template_name = 'inventory/form.html'
    login_url = '/accounts/login/'

    def get_success_url(self):
        messages.success(self.request, 'Lote atualizado com sucesso!')
        return reverse_lazy('inventory:dashboard')


class LoteDeleteView(LoginRequiredMixin, DeleteView):
    model = LoteEstoque
    template_name = 'inventory/lote_confirm_delete.html'
    success_url = reverse_lazy('inventory:dashboard')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lote excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


@method_decorator(require_POST, name='dispatch')
class ProdutoDeleteAjaxView(LoginRequiredMixin, DeleteView):
    model = Produto
    success_url = reverse_lazy('inventory:dashboard')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True, 'message': 'Produto excluído com sucesso!'})


@method_decorator(require_POST, name='dispatch')
class LoteDeleteAjaxView(LoginRequiredMixin, DeleteView):
    model = LoteEstoque
    success_url = reverse_lazy('inventory:dashboard')
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True, 'message': 'Lote excluído com sucesso!'})


def home_redirect(request):
    return redirect('inventory:dashboard')
