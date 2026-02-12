from django.urls import path
from .views import DashboardView, ProdutoCreateView, LoteCreateView

app_name = 'inventory'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('lotes/novo/', LoteCreateView.as_view(), name='lote-create'),
]
