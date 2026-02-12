from django.db import models
from django.utils import timezone


class Produto(models.Model):
    nome = models.CharField(max_length=120)
    sku = models.CharField(max_length=40, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.sku})'

    @property
    def quantidade_total(self):
        return sum(lote.quantidade for lote in self.lotes.all())


class LoteEstoque(models.Model):
    produto = models.ForeignKey(Produto, related_name='lotes', on_delete=models.CASCADE)
    codigo_lote = models.CharField(max_length=50)
    quantidade = models.PositiveIntegerField()
    data_vencimento = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_vencimento']
        unique_together = ('produto', 'codigo_lote')

    def __str__(self):
        return f'{self.produto.nome} - lote {self.codigo_lote}'

    @property
    def vencido(self):
        return self.data_vencimento < timezone.localdate()
