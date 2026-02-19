from django import forms
from django.core.exceptions import ValidationError
from .models import Produto, LoteEstoque


def validar_nome_produto(value):
    """Valida que o nome do produto não seja apenas números ou caracteres únicos."""
    if not value or len(value.strip()) < 2:
        raise ValidationError('O nome deve ter pelo menos 2 caracteres.')

    # Remove espaços para verificar se é apenas números
    valor_limpo = ''.join(value.split())
    if valor_limpo.isdigit():
        raise ValidationError('O nome não pode ser apenas números.')

    # Verifica se é apenas um caracter repetido
    if len(set(valor_limpo.lower())) == 1 and len(valor_limpo) > 1:
        raise ValidationError('O nome não pode ser apenas caracteres repetidos.')

    return value


class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(
        validators=[validar_nome_produto],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome do produto'
        })
    )

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição opcional do produto'
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo SKU do formulário pois será gerado automaticamente
        if 'sku' in self.fields:
            del self.fields['sku']


class LoteEstoqueForm(forms.ModelForm):
    class Meta:
        model = LoteEstoque
        fields = ['produto', 'quantidade', 'data_vencimento']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Quantidade em unidades'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo codigo_lote do formulário pois será gerado automaticamente
        if 'codigo_lote' in self.fields:
            del self.fields['codigo_lote']

        # Filtra apenas produtos ativos
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True)
