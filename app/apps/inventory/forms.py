from django import forms
from .models import Produto, LoteEstoque


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'sku', 'descricao', 'ativo']


class LoteEstoqueForm(forms.ModelForm):
    class Meta:
        model = LoteEstoque
        fields = ['produto', 'codigo_lote', 'quantidade', 'data_vencimento']
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
        }
