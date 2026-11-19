from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Cliente, OrdemServico
from .forms import (
    ClienteForm,
    OrdemServicoForm,
    UsuarioForm,
    UsuarioEdicaoForm
)


def usuario_e_administrador(user):

    return user.is_authenticated and (
        user.is_superuser
        or user.groups.filter(name='Administrador').exists()
    )


def acesso_negado(request):
    return render(request, 'acesso_negado.html')


@login_required
def home(request):

    grafico_status = [
        OrdemServico.objects.filter(status='aberta').count(),
        OrdemServico.objects.filter(status='andamento').count(),
        OrdemServico.objects.filter(status='fechada').count(),
    ]

    contexto = {
        'total_clientes': Cliente.objects.count(),

        'total_ordens': OrdemServico.objects.count(),

        'ordens_abertas': grafico_status[0],

        'ordens_andamento': grafico_status[1],

        'ordens_fechadas': grafico_status[2],

        'ultimos_clientes': (
            Cliente.objects
            .all()
            .order_by('-id')[:5]
        ),

        'ultimas_ordens': (
            OrdemServico.objects
            .select_related('cliente')
            .order_by('-id')[:5]
        ),

        'grafico_status': grafico_status,
    }

    return render(request, 'home.html', contexto)



# ========================================

# CLIENTES

# ========================================

@login_required
def clientes(request):

    busca = request.GET.get('busca', '').strip()

    clientes = Cliente.objects.all()

    if busca:

        filtros = (
            Q(nome__icontains=busca)
            | Q(telefone__icontains=busca)
            | Q(email__icontains=busca)
        )

        clientes = clientes.filter(filtros)

    clientes = clientes.order_by('-id')

    form = ClienteForm()

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('clientes')

    return render(request, 'clientes.html', {
        'clientes': clientes,
        'form': form,
        'busca': busca
    })


# EDITAR

@login_required
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    form = ClienteForm(instance=cliente)

    if request.method == 'POST':

        form = ClienteForm(
            request.POST,
            instance=cliente
        )

        if form.is_valid():

            form.save()

            return redirect('clientes')

    return render(request, 'editar_cliente.html', {
        'form': form
    })

# EXCLUIR CLIENTE

@user_passes_test(
    usuario_e_administrador,
    login_url='acesso_negado'
)
def excluir_cliente(request, id):

    cliente = get_object_or_404(
        Cliente,
        id=id
    )

    if request.method == 'POST':

        cliente.delete()

        return redirect('clientes')

    return render(request, 'excluir_cliente.html', {
        'cliente': cliente
    })

# EXCLUIR USUÁRIO

@user_passes_test(
    usuario_e_administrador,
    login_url='acesso_negado'
)
def excluir_usuario(request, id):

    usuario = get_object_or_404(
        User,
        id=id
    )

    motivo_bloqueio = None

    # 1. Impedir exclusão de superusuário
    if usuario.is_superuser:

        motivo_bloqueio = (
            'Este usuário é um superusuário e não pode ser excluído '
            'por esta tela.'
        )

    # 2. Impedir que o usuário exclua a própria conta
    elif usuario.id == request.user.id:

        motivo_bloqueio = (
            'Você não pode excluir sua própria conta.'
        )

    # 3. Impedir exclusão do último Administrador ativo
    elif (
        usuario.is_active
        and usuario.groups.filter(name='Administrador').exists()
    ):

        outro_administrador = (
            User.objects
            .filter(
                is_active=True,
                groups__name='Administrador'
            )
            .exclude(id=usuario.id)
            .exists()
        )

        if not outro_administrador:

            motivo_bloqueio = (
                'Este é o último Administrador ativo. '
                'Cadastre ou ative outro Administrador antes '
                'de realizar esta exclusão.'
            )

    # Se houver bloqueio, não permite excluir
    if motivo_bloqueio:

        return render(request, 'excluir_usuario.html', {
            'usuario': usuario,
            'motivo_bloqueio': motivo_bloqueio,
            'pode_excluir': False
        })

    # Exclusão somente por POST
    if request.method == 'POST':

        usuario.delete()

        return redirect('usuarios')

    return render(request, 'excluir_usuario.html', {
        'usuario': usuario,
        'pode_excluir': True
    })


# ========================================

# ORDENS DE SERVIÇO

# ========================================

@login_required
def ordens(request):

    busca = request.GET.get('busca', '').strip()

    ordens = OrdemServico.objects.select_related(
        'cliente'
    ).all()

    if busca:

        filtros = (
            Q(cliente__nome__icontains=busca)
            | Q(equipamento__icontains=busca)
            | Q(marca__icontains=busca)
            | Q(modelo__icontains=busca)
        )

        # Permitir pesquisa pelo número da OS
        if busca.isdigit():
            filtros |= Q(id=int(busca))

        ordens = ordens.filter(filtros)

    ordens = ordens.order_by('-id')

    return render(request, 'ordens.html', {
        'ordens': ordens,
        'busca': busca
    })


# CRIAR

@login_required
def nova_ordem(request):

    form = OrdemServicoForm()

    if request.method == 'POST':

        form = OrdemServicoForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('ordens')

    return render(request, 'nova_ordem.html', {
        'form': form
    })


# EDITAR

@login_required
def editar_ordem(request, id):

    ordem = get_object_or_404(
        OrdemServico,
        id=id
    )

    form = OrdemServicoForm(
        instance=ordem
    )

    if request.method == 'POST':

        form = OrdemServicoForm(
            request.POST,
            instance=ordem
        )

        if form.is_valid():

            form.save()

            return redirect('ordens')

    return render(request, 'editar_ordem.html', {
        'form': form
    })


# EXCLUIR


@user_passes_test(usuario_e_administrador, login_url='acesso_negado')
def excluir_ordem(request, id):

    ordem = get_object_or_404(
        OrdemServico,
        id=id
    )

    if request.method == 'POST':

        ordem.delete()

        return redirect('ordens')

    return render(request, 'excluir_ordem.html', {
        'ordem': ordem
    })


# DETALHAR
@login_required
def detalhar_ordem(request, id):

    ordem = get_object_or_404(
        OrdemServico,
        id=id
    )

    return render(request, 'detalhar_ordem.html', {
        'ordem': ordem
    })

@login_required
def imprimir_ordem(request, id):
    ordem = get_object_or_404(OrdemServico, id=id)
    return render(request, 'imprimir_ordem.html', {'ordem': ordem})


# ========================================

# DASHBOARD

# ========================================

@login_required
def dashboard(request):

    grafico_status = [
        OrdemServico.objects.filter(
            status='aberta'
        ).count(),

        OrdemServico.objects.filter(
            status='andamento'
        ).count(),

        OrdemServico.objects.filter(
            status='fechada'
        ).count(),
    ]

    contexto = {

        'total_clientes': Cliente.objects.count(),

        'total_ordens': OrdemServico.objects.count(),

        'ordens_abertas': OrdemServico.objects.filter(
            status='aberta'
        ).count(),

        'ordens_andamento': OrdemServico.objects.filter(
            status='andamento'
        ).count(),

        'ordens_fechadas': OrdemServico.objects.filter(
            status='fechada'
        ).count(),

        'ultimos_clientes': (
            Cliente.objects
            .all()
            .order_by('-id')[:5]
        ),

        'ultimas_ordens': (
            OrdemServico.objects
            .all()
            .order_by('-id')[:5]
        ),

        'grafico_status': grafico_status,
    }

    return render(
        request,
        'dashboard.html',
        contexto
    )


# ========================================

# USUÁRIOS

# ========================================

@user_passes_test(
    usuario_e_administrador,
    login_url='acesso_negado'
)
def usuarios(request):

    usuarios = User.objects.all().order_by('username')

    form = UsuarioForm()

    if request.method == 'POST':

        form = UsuarioForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('usuarios')

    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'form': form
    })

# EDITAR USUÁRIO

@user_passes_test(
    usuario_e_administrador,
    login_url='acesso_negado'
)
def editar_usuario(request, id):

    usuario = get_object_or_404(
        User,
        id=id
    )

    if request.method == 'POST':

        form = UsuarioEdicaoForm(
            request.POST,
            instance=usuario
        )

        if form.is_valid():

            form.save()

            return redirect('usuarios')

    else:

        form = UsuarioEdicaoForm(
            instance=usuario
        )

    return render(request, 'editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })