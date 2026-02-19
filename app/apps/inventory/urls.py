from django.urls import path
from .views import (
    DashboardView, ProdutoCreateView, LoteCreateView, RegisterView, HomeView,
    ProdutoUpdateView, ProdutoDeleteView, LoteUpdateView, LoteDeleteView,
    ProdutoDeleteAjaxView, LoteDeleteAjaxView
)

app_name = 'inventory'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('produtos/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('produtos/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produtos/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='produto-delete'),
    path('produtos/<int:pk>/deletar-ajax/', ProdutoDeleteAjaxView.as_view(), name='produto-delete-ajax'),
    path('lotes/novo/', LoteCreateView.as_view(), name='lote-create'),
    path('lotes/<int:pk>/editar/', LoteUpdateView.as_view(), name='lote-update'),
    path('lotes/<int:pk>/deletar/', LoteDeleteView.as_view(), name='lote-delete'),
    path('lotes/<int:pk>/deletar-ajax/', LoteDeleteAjaxView.as_view(), name='lote-delete-ajax'),
    path('register/', RegisterView.as_view(), name='register'),
]
