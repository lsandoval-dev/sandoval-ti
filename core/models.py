from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class OrdemServico(models.Model):

    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('andamento', 'Em andamento'),
        ('fechada', 'Fechada'),
    ]


    EQUIPAMENTO_CHOICES = [
        ('Notebook', 'Notebook'),
        ('Computador', 'Computador'),
        ('Impressora', 'Impressora'),
        ('Outro', 'Outro'),
    ]


    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    equipamento = models.CharField(
        max_length=50,
        choices=EQUIPAMENTO_CHOICES
    )

    marca = models.CharField(
        max_length=50,
        blank=True
    )

    modelo = models.CharField(
        max_length=100,
        blank=True
    )

    numero_serie = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número de série'
    )

    acessorios = models.TextField(
        blank=True,
        verbose_name='Acessórios recebidos'
    )

    estado_fisico = models.TextField(
        blank=True,
        verbose_name='Estado físico do equipamento'
    )

    problema = models.TextField()


    diagnostico = models.TextField(
        blank=True
    )

    servico_realizado = models.TextField(
        blank=True
    )


    valor = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )


    observacoes = models.TextField(
        blank=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberta'
    )


    criado_em = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"OS #{self.id} - {self.cliente.nome}"