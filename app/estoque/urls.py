from django.urls import path

from .views import DashboardView, MovimentarEstoqueView

app_name = 'estoque'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('frutas/<uuid:fruta_id>/movimentar/', MovimentarEstoqueView.as_view(), name='movimentar-estoque'),
]
