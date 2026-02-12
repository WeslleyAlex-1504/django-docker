# Projeto Fruteira - Backend Django

Estrutura inicial de um projeto Django com Docker, PostgreSQL e variáveis de ambiente.

## Tecnologias

- Python 3.12
- Django 5.0
- PostgreSQL 16
- Docker & Docker Compose

## Estrutura do Projeto

```
django-docker/
├── app/
│   ├── apps/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── asgi.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   └── inventory/
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── templates/
│   ├── manage.py
│   ├── requirements.txt
│   └── __init__.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

## Como Usar

### 1. Clonar o Repositório

```bash
git clone <seu-repo>
cd django-docker
```

### 2. Configurar Variáveis de Ambiente

O arquivo `.env` já contém valores padrão. Para produção, altere:

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-segura
POSTGRES_PASSWORD=senha-forte
```

### 3. Construir e Executar com Docker

```bash
docker-compose up --build
```

O Django estará disponível em `http://localhost:8000`

### 4. Executar Comandos Django

```bash
# Criar migração
docker-compose exec web python manage.py makemigrations

# Aplicar migração
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Acessar o Admin

- URL: `http://localhost:8000/admin`
- Credenciais: Usar as criadas no passo anterior

## Parar os Containers

```bash
docker-compose down
```


## Funcionalidades implementadas (cadastro/estoque/vencimento)

- Cadastro de **produtos** (nome, SKU, descrição e status ativo).
- Cadastro de **lotes de estoque** com quantidade e data de vencimento.
- Painel em `/estoque/` com:
  - total de produtos cadastrados,
  - total de itens em estoque,
  - lotes vencidos e próximos do vencimento (30 dias).
- Administração completa no Django Admin para produtos e lotes.

## Próximos Passos

1. Criar apps Django dentro de `app/apps/`
2. Registrar apps em `INSTALLED_APPS` no `settings.py`
3. Criar modelos e migração
4. Implementar views, URLs e templates

## Notas

- O banco de dados PostgreSQL persiste em volumes Docker
- Os arquivos da aplicação estão em volume para desenvolvimento (hot-reload)
- O Django está configurado para rodar em `0.0.0.0:8000` permitindo acesso externo

## Troubleshooting

### Porta 8000 já em uso
```bash
docker-compose down
docker system prune
docker-compose up
```

### Banco de dados não conecta
Verifique se o serviço `db` está saudável:
```bash
docker-compose ps
```

### Limpar volume do banco
```bash
docker-compose down -v
```
