from django import forms
from .models import Transacao
from .models import Categoria

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['tipo', 'categoria', 'descricao', 'valor', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),  # Define que o campo 'data' será um campo de data
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': 'R$ 0,00'}),  # Valor como número com 2 casas decimais
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
