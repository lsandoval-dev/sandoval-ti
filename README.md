# Sandoval TI — Sistema de Gerenciamento de Assistência Técnica

Sistema web desenvolvido com Python e Django para gerenciamento de clientes e Ordens de Serviço (OS).

O projeto tem como objetivo organizar o atendimento, acompanhar serviços e facilitar o controle das atividades de uma assistência técnica.

## Funcionalidades

- Cadastro, consulta, edição e exclusão de clientes.
- Cadastro e gerenciamento de Ordens de Serviço.
- Associação de clientes às respectivas Ordens de Serviço.
- Registro de equipamentos, marcas, modelos e números de série.
- Registro de acessórios e estado físico dos equipamentos.
- Acompanhamento do status das Ordens de Serviço.
- Edição e consulta de serviços realizados.
- Geração de Ordem de Serviço em PDF.
- Dashboard com indicadores e resumo das atividades.
- Gerenciamento de usuários.
- Controle de permissões por perfil: Administrador e Técnico.
- Pesquisa de clientes e Ordens de Serviço.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap 5
- Bootstrap Icons
- JavaScript

## Requisitos

- Python 3.12 ou superior, compatível com a versão do Django utilizada.
- Git.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/lsandoval-dev/sandoval-ti.git
```

Entre na pasta do projeto:

```bash
cd sandoval-ti
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Config