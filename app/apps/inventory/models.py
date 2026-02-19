from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Produto(models.Model):
    nome = models.CharField(max_length=120, validators=[])
    sku = models.CharField(max_length=40, unique=True, blank=True)
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
    codigo_lote = models.CharField(max_length=50, blank=True)
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


@receiver(pre_save, sender=Produto)
def gerar_sku_automatico(sender, instance, **kwargs):
    """Gera SKU automático no formato 001, 002, 003..."""
    if not instance.sku:
        # Pega o último SKU numérico
        ultimo_produto = Produto.objects.filter(
            sku__regex=r'^\d+$'
        ).order_by('-sku').first()

        if ultimo_produto:
            try:
                ultimo_numero = int(ultimo_produto.sku)
                novo_numero = ultimo_numero + 1
            except ValueError:
                novo_numero = 1
        else:
            novo_numero = 1

        instance.sku = f"{novo_numero:03d}"


@receiver(pre_save, sender=LoteEstoque)
def gerar_codigo_lote_automatico(sender, instance, **kwargs):
    """Gera código do lote automático baseado no produto"""
    if not instance.codigo_lote:
        # Conta quantos lotes já existem para este produto
        quantidade_lotes = LoteEstoque.objects.filter(produto=instance.produto).count()
        instance.codigo_lote = f"{instance.produto.sku}-{quantidade_lotes + 1:02d}"
