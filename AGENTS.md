# AGENTS.md — Oferte

## Contexto do Projeto

Aplicativo de gestão de igreja para controle de usuários, dizimistas e ofertas.

**Escopo** (definido em `Oferte.txt`):
- Tela de login
- CRUD de Usuários (nome, CPF, telefone, e-mail, cargo admin/dizimista, ativo/inativo, dizimista/não dizimista)
- Listagem de Dizimistas com status (ofertou / não ofertou no mês)
- CRUD de Ofertas (valor, dizimista, data, tipo pagamento dinheiro/cartão/PIX)
- Histórico geral de ofertas + listagem individual por dizimista
- Configuração da igreja (nome, CNPJ, endereço)
- Alteração de senha e dados pessoais
- Acessibilidade: tema com cor personalizável pelo usuário

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.14+ / Django 6.0.6 |
| API | Django REST Framework 3.17 + JWT (djangorestframework-simplejwt 5.5) |
| Banco | SQLite |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Design System | CSS próprio inspirado no Flutter/Material Design 3 |
| Templates | Django Templates com interatividade via `fetch()` para API |

## Estrutura de Diretórios

```
oferte/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── AGENTS.md
├── PLANO.md
├── Oferte.txt
├── core/                     # Projeto Django (settings, urls, wsgi, asgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── context_processors.py  # Injeta user_profile e theme_color nos templates
├── accounts/                 # App: autenticação e usuários
│   ├── models.py             # User customizado (AbstractBaseUser + PermissionsMixin)
│   ├── serializers.py        # UserSerializer, LoginSerializer, ChangePasswordSerializer
│   ├── views.py              # LoginView, LogoutView, UserViewSet, ProfileView
│   ├── views_pages.py        # TemplateView para todas as páginas frontend
│   ├── urls.py               # Rotas da API + login page
│   ├── admin.py
│   ├── management/commands/seed_data.py
│   └── templates/accounts/
│       ├── usuario_list.html
│       └── usuario_form.html
├── ofertas/                  # App: ofertas
│   ├── models.py             # Oferta (valor, dizimista FK, data, tipo_pagamento)
│   ├── serializers.py        # OfertaSerializer
│   ├── views.py              # OfertaViewSet (CRUD + filtros)
│   ├── urls.py
│   ├── admin.py
│   └── templates/ofertas/
│       ├── oferta_list.html
│       ├── oferta_form.html
│       └── oferta_dizimista.html
├── dizimistas/               # App: listagem de dizimistas
│   ├── models.py             # Reusa User (is_dizimista=True)
│   ├── serializers.py        # DizimistaListSerializer (com métricas)
│   ├── views.py              # DizimistaListView (GET, filtro mês/ano)
│   ├── urls.py
│   └── templates/dizimistas/
│       └── dizimista_list.html
├── configapp/                # App: configurações
│   ├── models.py             # ConfiguracaoIgreja (singleton) + UserProfile (OneToOne)
│   ├── serializers.py        # ConfiguracaoIgrejaSerializer, UserProfileSerializer
│   ├── views.py              # ConfiguracaoIgrejaView, UserProfileView, ChangePasswordView
│   ├── urls.py
│   ├── admin.py
│   └── templates/configapp/
│       ├── igreja_config.html
│       ├── tema_config.html
│       ├── profile.html
│       └── change_password.html
├── templates/
│   ├── base.html             # Sidebar + bottom-nav + progress + snackbar + scripts
│   ├── registration/login.html
│   └── pages/
│       ├── dashboard.html
│       └── configuracoes.html
└── static/
    └── (servido pelo Django em DEBUG, coletado em STATIC_ROOT em produção)
        ├── css/
        │   ├── material-theme.css   # Design system MD3 completo
        │   ├── components.css       # Utilitários, animações, grades
        │   └── responsive.css       # 3 breakpoints (≥1024, 768-1023, <768)
        ├── js/
        │   ├── api.js               # Cliente HTTP com JWT (localStorage)
        │   ├── theme.js             # Tema, autenticação, formatação
        │   ├── components.js        # Ripple, Snackbar, Dialog, máscaras, validação
        │   └── pages/
        │       ├── login.js
        │       ├── dashboard.js
        │       ├── usuarios.js
        │       ├── usuario-form.js
        │       ├── dizimistas.js
        │       ├── ofertas.js
        │       ├── oferta-form.js
        │       ├── oferta-dizimista.js
        │       ├── igreja-config.js
        │       ├── tema-config.js
        │       ├── profile.js
        │       └── change-password.js
        ├── webfonts/
        └── img/
```

## Modelos de Dados

### User (accounts)
- `nome`, `cpf` (unique), `telefone`, `email` (unique, USERNAME_FIELD)
- `cargo` (admin/dizimista), `is_active`, `is_dizimista`, `is_staff`
- `date_joined` (auto_now_add)
- Herda `AbstractBaseUser` + `PermissionsMixin`
- Manager: `UserManager` com `create_user` e `create_superuser`
- `REQUIRED_FIELDS = ['nome', 'cpf']`

### Oferta (ofertas)
- `valor` (Decimal max_digits=10, decimal_places=2)
- `dizimista` (FK → User, related_name='ofertas', on_delete=CASCADE)
- `data` (DateField)
- `tipo_pagamento` (choices: dinheiro/cartao/pix)
- `created_at`, `updated_at` (auto_now_add/auto_now)

### ConfiguracaoIgreja (configapp)
- Singleton (pk=1 forçado via override do `save`)
- `nome`, `cnpj`, `endereco`
- Helper classmethod `get_instance()` para obter/criar o singleton

### UserProfile (configapp)
- `user` (OneToOne → User, related_name='profile')
- `theme_primary_color` (CharField max_length=7, default `#6750A4`)
- Signal `post_save` cria UserProfile automaticamente ao criar User

## API REST (DRF)

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/auth/login/` | Login → JWT (access + refresh + user) |
| POST | `/api/auth/logout/` | Logout |
| GET/PUT | `/api/auth/profile/` | Dados do usuário logado (inclui theme_primary_color) |
| POST | `/api/auth/change-password/` | Alterar senha |
| GET/POST | `/api/usuarios/` | Listar/criar usuários (com paginação) |
| GET/PUT/DELETE | `/api/usuarios/<id>/` | Detalhar/editar/deletar |
| GET | `/api/usuarios/?search=&cargo=&ativos=&is_dizimista=` | Filtrar usuários |
| GET | `/api/dizimistas/` | Listar dizimistas com status de oferta |
| GET | `/api/dizimistas/?mes=&ano=` | Filtrar por mês/ano |
| GET/POST | `/api/ofertas/` | Listar/criar ofertas |
| GET/PUT/DELETE | `/api/ofertas/<id>/` | Detalhar/editar/deletar |
| GET | `/api/ofertas/?dizimista=&data__gte=&data__lte=&tipo_pagamento=` | Filtrar ofertas |
| GET/PUT | `/api/configuracao/igreja/` | Dados da igreja (singleton) |
| GET/PUT | `/api/configuracao/tema/` | Cor do tema do usuário |

## Páginas Frontend

| Rota | Template | JS | Descrição |
|---|---|---|---|
| `/login/` | `registration/login.html` | `login.js` | Login com JWT |
| `/` | `pages/dashboard.html` | `dashboard.js` | Resumo + gráfico 6 meses |
| `/usuarios/` | `accounts/usuario_list.html` | `usuarios.js` | Listagem com busca/filtros |
| `/usuarios/novo/` | `accounts/usuario_form.html` | `usuario-form.js` | Cadastro |
| `/usuarios/<id>/` | `accounts/usuario_form.html` | `usuario-form.js` | Edição |
| `/dizimistas/` | `dizimistas/dizimista_list.html` | `dizimistas.js` | Grid com status |
| `/ofertas/` | `ofertas/oferta_list.html` | `ofertas.js` | Listagem + totalizador |
| `/ofertas/nova/` | `ofertas/oferta_form.html` | `oferta-form.js` | Cadastro |
| `/ofertas/<id>/` | `ofertas/oferta_form.html` | `oferta-form.js` | Edição |
| `/ofertas/dizimista/<id>/` | `ofertas/oferta_dizimista.html` | `oferta-dizimista.js` | Ofertas por dizimista |
| `/configuracoes/` | `pages/configuracoes.html` | — | Menu de configurações |
| `/configuracoes/igreja/` | `configapp/igreja_config.html` | `igreja-config.js` | Dados da igreja |
| `/configuracoes/tema/` | `configapp/tema_config.html` | `tema-config.js` | Cor do tema + preview |
| `/perfil/` | `configapp/profile.html` | `profile.js` | Dados pessoais |
| `/alterar-senha/` | `configapp/change_password.html` | `change-password.js` | Trocar senha |

## Autenticação

- **JWT exclusivo** (sem sessão Django)
- Token armazenado em `localStorage` (`access_token`, `refresh_token`)
- `api.js` anexa `Authorization: Bearer <token>` automaticamente
- Em 401, limpa tokens e redireciona para `/login/`
- `theme.js` redireciona para `/login/` se não houver token (exceto na própria página de login)
- Sidebar e bottom-nav são sempre renderizados no HTML; na página de login são ocultados via classe CSS `.is-login-page`
- Nome do usuário na sidebar é populado via JS (`api.getUser()`)

## Design System CSS

Framework próprio no padrão `.md-*` (Material Design 3), inspirado no Flutter:

### Componentes
- `.md-app-bar` — AppBar superior com título + ações
- `.md-bottom-nav` — BottomNavigationBar (mobile, 5 itens)
- `.md-card`, `.md-card--elevated`, `.md-card--filled`
- `.md-btn`, `.md-btn--filled`, `.md-btn--tonal`, `.md-btn--outlined`, `.md-btn--danger`, `.md-btn--small`
- `.md-fab` — FloatingActionButton
- `.md-text-field` — Input com label flutuante (suporta textarea, erro)
- `.md-dropdown` — Select estilizado com seta
- `.md-chip`, `.md-chip--success`, `.md-chip--error`, `.md-chip--warning`, `.md-chip--info`
- `.md-switch` — Toggle switch customizado
- `.md-table` — Data table (em mobile vira cards)
- `.md-dialog` — Modal de confirmação (overlay + scale animation)
- `.md-snackbar`, `.md-snackbar--success`, `.md-snackbar--error`
- `.md-progress` — Barra de progresso linear animada
- `.md-list-tile` — ListItem com título/subtítulo
- `.md-divider`
- `.md-badge` — Contadores
- `.md-avatar` — Círculo colorido com iniciais
- `.md-pagination` — Navegação de páginas
- `.md-summary-card` — Card de destaque (totalizador)
- `.md-empty-state` — Estado vazio com ícone e mensagem
- `.md-ripple` — Efeito ripple (ativado via JS)
- `.md-tooltip` — Tooltip em hover

### Tokens CSS
- `--md-sys-color-primary` (customizável pelo usuário)
- `--md-sys-color-on-primary`, `--md-sys-color-primary-container`, `--md-sys-color-on-primary-container`
- `--md-sys-color-secondary`, `--md-sys-color-surface`, `--md-sys-color-surface-variant`
- `--md-sys-color-error`, `--md-sys-color-error-container`
- `--md-sys-color-outline`, `--md-sys-color-background`, `--md-sys-color-on-background`
- `--md-sys-elevation-level0/1/2/3`
- `--md-sys-shape-small/medium/large/extra-large`
- `--md-sys-font-family` (Roboto)

### Utilitários (components.css)
- Margem: `.mt-*`, `.mb-*`
- Padding: `.p-*`
- Gap: `.gap-*`
- Flex: `.flex`, `.flex-center`, `.flex-between`, `.flex-col`, `.flex-1`
- Texto: `.text-center`, `.text-muted`, `.text-primary`, `.text-error`, `.text-success`
- Tamanhos: `.text-small`, `.text-medium`, `.text-large`, `.text-xlarge`
- Borda: `.rounded-small/medium/large/full`
- Outros: `.truncate`, `.w-full`, `.bg-surface`, `.cursor-pointer`

### Layouts específicos
- `.filter-bar`, `.filter-group`, `.filter-checkbox`
- `.color-grid`, `.color-grid__item—active`
- `.theme-preview`
- `.dizimista-grid` (grid de cards responsivo)
- `.summary-row` (cards de resumo lado a lado)
- `.chart-bars`, `.chart-bar`, `.chart-bar__label` (gráfico CSS puro)
- `.view-toggle` (alternar visualização)

## Responsividade

| Breakpoint | Sidebar | BottomNav | Tabelas |
|---|---|---|---|
| ≥ 1024px | Fixa 280px | Oculta | Normal |
| 768–1023px | Mini 72px (só ícones) | Oculta | Normal |
| < 768px | Oculta | 5 ícones + labels | Cards por linha |

## Convenções de Código

- **Python**: PEP 8, snake_case
- **CSS**: BEM adaptado — `.md-componente`, `.md-componente--modificador`
- **JavaScript**: camelCase, `const`/`let`, funções descritivas, async/await
- **Templates Django**: snake_case para blocos e arquivos
- **Autenticação**: JWT via localStorage (sem sessão Django)
- **Commits**: português, imperativo ("Adiciona tela de login")

## Comandos Úteis

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Seed: admin@igreja.com / 123456 (15 dizimistas, ~49 ofertas)

Ordem de apps (dependências): `accounts` → `ofertas` → `dizimistas` → `configapp`

---

*Atualizar este arquivo sempre que houver mudanças significativas na estrutura, modelos, API ou convenções do projeto.*
