from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Fruta


class FrutaModelTests(TestCase):
    def test_status_vencida(self):
        fruta = Fruta.objects.create(
            nome='Banana',
            tipo=Fruta.Tipo.TROPICAL,
            data_validade=timezone.localdate() - timedelta(days=1),
            quantidade_estoque=5,
        )
        self.assertEqual(fruta.status, Fruta.Status.VENCIDA)

    def test_saida_nao_permite_estoque_negativo(self):
        fruta = Fruta.objects.create(
            nome='Laranja',
            tipo=Fruta.Tipo.CITRICA,
            data_validade=timezone.localdate() + timedelta(days=7),
            quantidade_estoque=2,
        )
        with self.assertRaises(ValidationError):
            fruta.saida_estoque(3)
