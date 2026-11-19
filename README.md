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
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd assistencia
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

## Configuração

Crie o arquivo `.env` na pasta principal do projeto.

Gere uma chave secreta e salve no arquivo usando o PowerShell:

```powershell
$key = python -c "import secrets; print(secrets.token_urlsafe(50))"
Set-Content -Path .env -Value "DJANGO_SECRET_KEY=$key" -Encoding ascii
```

## Banco de dados

Execute as migrações:

```bash
python manage.py migrate
```

Crie o primeiro usuário administrador:

```bash
python manage.py createsuperuser
```

## Executando o projeto

Inicie o servidor local:

```bash
python manage.py runserver
```

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Observações

Este projeto foi desenvolvido para fins de aprendizado, prática e portfólio profissional.

A versão disponibilizada utiliza SQLite e está preparada para execução local. Não representa uma implantação em ambiente de produção.

## Autor

**Ladislau Sandoval**

Desenvolvimento com Python e Django.