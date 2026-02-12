from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import LoteEstoque, Produto


class InventoryTests(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse('inventory:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_produto_quantidade_total(self):
        produto = Produto.objects.create(nome='Maçã', sku='MACA-001')
        LoteEstoque.objects.create(
            produto=produto,
            codigo_lote='L1',
            quantidade=5,
            data_vencimento=timezone.localdate() + timedelta(days=5),
        )
        LoteEstoque.objects.create(
            produto=produto,
            codigo_lote='L2',
            quantidade=7,
            data_vencimento=timezone.localdate() + timedelta(days=10),
        )

        self.assertEqual(produto.quantidade_total, 12)
