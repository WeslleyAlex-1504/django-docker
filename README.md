# Fruteira - Cadastro e Controle de Estoque

Aplicação web em Django para gestão de frutas com foco em cadastro, estoque e vencimento. O projeto foi estruturado para uso profissional, com separação de ambientes, Docker, PostgreSQL e integração pronta para Sentry.

## Stack utilizada

- Python 3.12
- Django 5+
- PostgreSQL
- Docker e Docker Compose
- Sentry (monitoramento de erros)
- Git + GitHub
- `pip` para gerenciamento de dependências

### Por que `pip` neste projeto?
O projeto usa `pip` com `requirements.txt` por simplicidade operacional em ambientes de aula/equipe inicial e por integração direta com Docker cache em build de imagem.

## Estrutura do projeto

```bash
fruteira/
├── app/
│   ├── core/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── estoque/
│   │   ├── migrations/
│   │   ├── templates/estoque/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── urls_api.py
│   │   └── admin.py
│   ├── users/
│   └── manage.py
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── app/requirements.txt
```

### Papel de cada pasta/arquivo
- `app/core/settings/base.py`: configurações compartilhadas (apps, middleware, DB, Sentry).
- `app/core/settings/dev.py`: ajustes de desenvolvimento.
- `app/core/settings/prod.py`: endurecimento de segurança para produção.
- `app/estoque/models.py`: regras de domínio da fruta e estoque.
- `app/estoque/views.py`: dashboard e endpoints de movimentação/API.
- `app/estoque/serializers.py`: serialização para resposta JSON.
- `docker/Dockerfile`: build multi-stage, imagem enxuta e cache eficiente.
- `docker/entrypoint.sh`: espera banco, roda migrations e staticfiles automaticamente.
- `.env.example`: variáveis padrão para configuração local.

## Requisitos funcionais implementados

### Cadastro de frutas
Cada fruta possui:
- Nome
- Tipo (cítrica, tropical, vermelha, climatérica, outra)
- Data de validade
- Quantidade em estoque
- Data de cadastro (`created_at`)
- Status (ativa / vencida / esgotada)

### Estoque
- Entrada de estoque (`entrada_estoque`)
- Saída de estoque (`saida_estoque`)
- Atualização automática de status
- Validação contra estoque negativo

### Regras de modelo (boas práticas)
- UUID como chave primária
- `created_at` e `updated_at`
- Método de domínio `is_vencida()`

## Como rodar com Docker

1. Copie variáveis de ambiente:

```bash
cp .env.example .env
```

2. Suba os serviços:

```bash
docker compose up --build
```

3. Acesse:
- App: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API JSON: http://localhost:8000/api/frutas/

## Comandos úteis

```bash
# Criar migrations
docker compose exec web python manage.py makemigrations

# Aplicar migrations
docker compose exec web python manage.py migrate

# Criar superusuário
docker compose exec web python manage.py createsuperuser

# Rodar testes
docker compose exec web python manage.py test estoque
```

## Sentry

1. Crie um projeto Django no Sentry.
2. Defina `SENTRY_DSN` no `.env`.
3. Reinicie o container `web`.
4. Para testar captura de erro, você pode lançar manualmente uma exceção em uma view e acessar a rota.

A integração é carregada automaticamente quando o pacote `sentry-sdk` estiver instalado e o `SENTRY_DSN` estiver configurado.

## Git e GitHub

### Exemplo de commits organizados
- `feat: criar app estoque com regras de domínio`
- `chore: configurar docker multi-stage e entrypoint`
- `docs: atualizar README com setup completo`

### Publicação no GitHub
```bash
git init
git add .
git commit -m "feat: estrutura inicial da fruteira"
git branch -M main
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
```

Representante do grupo: basta usar as credenciais com permissão no repositório remoto e executar os comandos acima.
