import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Fruta(models.Model):
    class Tipo(models.TextChoices):
        CITRICA = 'citrica', 'Cítrica'
        TROPICAL = 'tropical', 'Tropical'
        VERMELHA = 'vermelha', 'Vermelha'
        CLIMATERICA = 'climaterica', 'Climatérica'
        OUTRA = 'outra', 'Outra'

    class Status(models.TextChoices):
        ATIVA = 'ativa', 'Ativa'
        VENCIDA = 'vencida', 'Vencida'
        ESGOTADA = 'esgotada', 'Esgotada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    data_validade = models.DateField()
    quantidade_estoque = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('data_validade', 'nome')

    def __str__(self):
        return f'{self.nome} ({self.quantidade_estoque})'

    def is_vencida(self):
        return self.data_validade < timezone.localdate()

    def atualizar_status(self, save=True):
        if self.is_vencida():
            self.status = self.Status.VENCIDA
        elif self.quantidade_estoque == 0:
            self.status = self.Status.ESGOTADA
        else:
            self.status = self.Status.ATIVA

        if save:
            self.save(update_fields=['status', 'updated_at'])

    def entrada_estoque(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A entrada de estoque deve ser maior que zero.')
        self.quantidade_estoque += quantidade
        self.atualizar_status(save=False)
        self.save(update_fields=['quantidade_estoque', 'status', 'updated_at'])

    def saida_estoque(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A saída de estoque deve ser maior que zero.')
        if quantidade > self.quantidade_estoque:
            raise ValidationError('Não é permitido estoque negativo.')
        self.quantidade_estoque -= quantidade
        self.atualizar_status(save=False)
        self.save(update_fields=['quantidade_estoque', 'status', 'updated_at'])

    def clean(self):
        if self.quantidade_estoque < 0:
            raise ValidationError('Quantidade em estoque não pode ser negativa.')

    def save(self, *args, **kwargs):
        self.atualizar_status(save=False)
        super().save(*args, **kwargs)
