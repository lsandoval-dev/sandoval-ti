
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

from .models import Cliente, OrdemServico


# ========================================
# CLIENTES
# ========================================

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            'nome',
            'telefone',
            'email'
        ]


# ========================================
# ORDENS DE SERVIÇO
# ========================================

class OrdemServicoForm(forms.ModelForm):

    class Meta:
        model = OrdemServico

        fields = [
            'cliente',
            'equipamento',
            'marca',
            'modelo',
            'numero_serie',
            'acessorios',
            'estado_fisico',
            'problema',
            'diagnostico',
            'servico_realizado',
            'valor',
            'observacoes',
            'status'
        ]

        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),

            'equipamento': forms.Select(attrs={
                'class': 'form-select'
            }),

            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Dell, Acer, HP...'
            }),

            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe o modelo do equipamento'
            }),

                'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Informe o número de série'
            }),

            'acessorios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ex: Carregador, fonte, cabos...'
            }),

            'estado_fisico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva as condições físicas do equipamento...'
            }),

            'problema': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva o problema informado pelo cliente...'
            }),

            'diagnostico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Informe o diagnóstico técnico...'
            }),

            'servico_realizado': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva o serviço realizado...'
            }),

            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 150.00'
            }),

            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações adicionais...'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


# ========================================
# USUÁRIOS - CRIAÇÃO
# ========================================

class UsuarioForm(UserCreationForm):

    perfil = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=['Administrador', 'Técnico']
        ),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Perfil do usuário'
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = [
            'username',
            'perfil'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome de usuário'
            }),
        }

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        perfil = self.cleaned_data['perfil']

        if commit:
            usuario.groups.set([perfil])

        return usuario


# ========================================
# USUÁRIOS - EDIÇÃO
# ========================================

class UsuarioEdicaoForm(forms.ModelForm):

    perfil = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=['Administrador', 'Técnico']
        ),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Perfil do usuário'
    )

    nova_senha = forms.CharField(
        required=False,
        label='Nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha (opcional)',
            'autocomplete': 'new-password'
        }),
        help_text='Deixe em branco para manter a senha atual.'
    )

    confirmar_senha = forms.CharField(
        required=False,
        label='Confirmar nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha novamente',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User

        fields = [
            'username',
            'perfil'
        ]

        labels = {
            'username': 'Nome de usuário'
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome de usuário'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['perfil'].initial = (
                self.instance.groups.filter(
                    name__in=['Administrador', 'Técnico']
                ).first()
            )

    def clean(self):
        dados = super().clean()

        nova_senha = dados.get('nova_senha')
        confirmar_senha = dados.get('confirmar_senha')

        if nova_senha or confirmar_senha:

            if not nova_senha:
                self.add_error(
                    'nova_senha',
                    'Digite a nova senha.'
                )

            if not confirmar_senha:
                self.add_error(
                    'confirmar_senha',
                    'Confirme a nova senha.'
                )

            if (
                nova_senha
                and confirmar_senha
                and nova_senha != confirmar_senha
            ):
                self.add_error(
                    'confirmar_senha',
                    'As senhas não coincidem.'
                )

        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)

        nova_senha = self.cleaned_data.get('nova_senha')

        if nova_senha:
            usuario.set_password(nova_senha)

        if commit:
            usuario.save()
            usuario.groups.set([self.cleaned_data['perfil']])

        return usuario
