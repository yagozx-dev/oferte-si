# Oferte — Plano de Implementação

Sistema de Gestão de Igreja
Backend: Python / Django / DRF / SQLite
Frontend: HTML / CSS / Vanilla JS (Design System Material Design 3 — Flutter-like)

---

## Sumário

- [Fase 1 — Fundação](#fase-1--fundao)
- [Fase 2 — App de Usuários](#fase-2--app-de-usurios)
- [Fase 3 — App de Ofertas](#fase-3--app-de-ofertas)
- [Fase 4 — App de Dizimistas](#fase-4--app-de-dizimistas)
- [Fase 5 — App de Configuração](#fase-5--app-de-configurao)
- [Fase 6 — Responsividade e Polimento](#fase-6--responsividade-e-polimento)
- [Fase 7 — Finalização](#fase-7--finalizao)

---

## Fase 1 — Fundação

### 1.1. Iniciar o projeto Django

- [ ] Instalar dependências: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `python-decouple`
- [ ] Criar projeto Django: `django-admin startproject core .`
- [ ] Configurar `settings.py`:
  - `INSTALLED_APPS` com `rest_framework`, `rest_framework_simplejwt`
  - Configurar `AUTH_USER_MODEL = 'accounts.User'`
  - Configurar DRF com `DEFAULT_AUTHENTICATION_CLASSES` (JWT)
  - Configurar `STATICFILES_DIRS`, `MEDIA_ROOT`, `MEDIA_URL`
  - Adicionar `python-decouple` para variáveis de ambiente
- [ ] Criar arquivo `.env` com `SECRET_KEY` e `DEBUG=True`
- [ ] Criar `requirements.txt`

### 1.2. Criar estrutura de diretórios estáticos

- [ ] Criar `static/` com subpastas:
  - `static/css/`
  - `static/js/`
  - `static/js/pages/`
  - `static/img/`
  - `static/webfonts/`
- [ ] Baixar Material Icones (Google Fonts) — arquivos WOFF2
- [ ] Baixar Roboto (Google Fonts) — arquivos WOFF2

### 1.3. Design System CSS (Material Design 3 — Flutter-like)

- [ ] Criar `static/css/material-theme.css`:
  - Definir tokens de design (variáveis CSS): cores, elevação, shape, tipografia
  - `.md-app-bar` — barra superior com título e ações
  - `.md-bottom-nav` — navegação inferior estilo Flutter
  - `.md-card`, `.md-card--elevated`, `.md-card--filled`
  - `.md-btn`, `.md-btn--filled`, `.md-btn--tonal`, `.md-btn--outlined`
  - `.md-fab` — FloatingActionButton
  - `.md-text-field` — campo de texto com label flutuante
  - `.md-dropdown` — select estilizado
  - `.md-chip` — tags/chips
  - `.md-dialog`, `.md-snackbar`
  - `.md-list-tile` — listas estilo ListTile
  - `.md-divider`
  - `.md-switch` — toggle switch
  - `.md-progress` — barra de progresso linear
  - `.md-ripple` — efeito ripple (ativado via JS)
  - `.md-table` — tabela estilo DataTable
  - `.md-badge` — badges/contadores
- [ ] Criar `static/css/responsive.css`:
  - Breakpoints: `≥1024px` (desktop), `768px–1023px` (tablet), `<768px` (mobile)
  - `.sidebar` — sidebar fixa para desktop
  - `.sidebar--mini` — sidebar colapsada para tablet
  - `.hide-desktop`, `.hide-mobile`, `.hide-tablet`
  - Grid responsivo (`.md-row`, `.md-col`)
- [ ] Criar `static/css/components.css`:
  - Classes utilitárias (`.mt-*`, `.mb-*`, `.p-*`, `.gap-*`, `.flex-center`, etc.)
  - Animações de transição de página (`.page-enter`, `.page-leave`)
  - Animações de hover e foco

### 1.4. App de autenticação (`accounts`)

- [ ] Criar app: `python manage.py startapp accounts`
- [ ] Criar modelo `User` customizado (herdando `AbstractBaseUser` + `PermissionsMixin`):
  - Campos: `nome`, `cpf` (unique), `telefone`, `email` (unique, USERNAME_FIELD), `cargo` (admin/dizimista), `is_active`, `is_dizimista`
  - `objects = UserManager()`
  - `REQUIRED_FIELDS = ['nome', 'cpf']`
- [ ] Criar serializers: `UserSerializer`, `LoginSerializer`, `ChangePasswordSerializer`
- [ ] Criar viewsets: `UserViewSet` (CRUD completo)
- [ ] Criar views de autenticação: `LoginView` (retorna JWT), `LogoutView`
- [ ] Criar `accounts/urls.py` com rotas da API
- [ ] Registrar modelo no `admin.py`
- [ ] Fazer migrações: `makemigrations` + `migrate`
- [ ] Criar management command `seed_data` para popular dados de teste

### 1.5. Template base e tela de login

- [ ] Criar `templates/` raiz em `settings.py`
- [ ] Criar `templates/base.html`:
  - Estrutura HTML5 com `{% block title %}`, `{% block content %}`, `{% block scripts %}`
  - Inclusão de CSS global
  - Sidebar para desktop (links: Dashboard, Usuários, Dizimistas, Ofertas, Configurações)
  - BottomNav para mobile (5 ícones)
  - Container principal com transição de página
  - Injeção de cor do tema via `{% block extra_head %}` (variável CSS `--md-sys-color-primary` vinda do user logado)
  - Modal de confirmação (`.md-dialog`) e snackbar (`.md-snackbar`)
- [ ] Criar `templates/registration/login.html`:
  - Estendendo `base.html` (sem sidebar)
  - Formulário de login (email + senha)
  - Botão "Entrar" com `.md-btn--filled`
  - Link de "Esqueci senha" (placeholder)
- [ ] Criar `accounts/views.py` com `LoginPageView` (TemplateView)
- [ ] Criar URL para `/login/` no `core/urls.py`
- [ ] Criar `static/js/api.js`:
  - Função `api.get(url, token)`, `api.post(url, data, token)`, `api.put`, `api.delete`
  - Gerenciamento de token (localStorage)
  - Interceptor para erro 401 (redirecionar login)
- [ ] Criar `static/js/pages/login.js`: submit do form chamando API de login, armazenar token, redirecionar
- [ ] Criar `static/js/theme.js`: leitura do token, redirecionamento se não autenticado, troca de cor do tema dinâmica
- [ ] Criar `static/js/components.js`:
  - `mdRipple(container)` — aplica efeito ripple a elementos
  - `mdSnackbar(message, type)` — exibe notificação
  - `mdDialog(title, message, onConfirm)` — exibe diálogo de confirmação
  - `mdTogglePassword(fieldId)` — mostrar/esconder senha

### 1.6. Verificação da Fase 1

- [ ] Servidor roda sem erros
- [ ] Tela de login é exibida
- [ ] Login com credenciais seed funciona e retorna token
- [ ] Design system aparece corretamente (cards, botões, inputs)
- [ ] Sidebar aparece em desktop, bottom-nav em mobile (redimensionar navegador)

---

## Fase 2 — App de Usuários

### 2.1. API de Usuários (DRF)

- [ ] No serializer `UserSerializer`, adicionar campos: `nome`, `cpf`, `telefone`, `email`, `cargo`, `is_active`, `is_dizimista`, `password` (write-only)
- [ ] No `UserViewSet`: implementar `create` com hash de senha, `update` parcial
- [ ] Adicionar filtros: busca por nome, CPF, email, filtro por cargo, status ativo, status dizimista
- [ ] Rotas registradas via `DefaultRouter`

### 2.2. Template de Listagem de Usuários

- [ ] Criar `accounts/templates/accounts/usuario_list.html`:
  - AppBar com título "Usuários" + botão "Novo Usuário" (.md-btn--filled)
  - Campo de busca (.md-text-field com ícone de search)
  - Filtros: select de cargo, checkbox "Ativos apenas", checkbox "Dizimistas apenas"
  - Tabela (.md-table) com colunas: Nome, CPF, Telefone, E-mail, Cargo, Dizimista, Ativo, Ações (editar/deletar)
  - Paginação
  - FAB "Novo Usuário" visível apenas em mobile
- [ ] Criar `static/js/pages/usuarios.js`:
  - `listarUsuarios()` — GET `/api/usuarios/` com parâmetros de busca, preenche tabela
  - `deletarUsuario(id)` — confirma com mdDialog, depois DELETE, depois recarrega lista
  - Event listeners para busca e filtros (debounce no campo de busca)
  - Paginação via clique em números

### 2.3. Template de Formulário de Usuário

- [ ] Criar `accounts/templates/accounts/usuario_form.html`:
  - AppBar com título "Novo Usuário" ou "Editar Usuário" conforme contexto
  - Card (.md-card--elevated) com formulário:
    - Campo Nome (.md-text-field)
    - Campo CPF (.md-text-field com máscara `___.___.___-__`)
    - Campo Telefone (.md-text-field com máscara `(__) _____-____`)
    - Campo E-mail (.md-text-field com type email)
    - Select Cargo (.md-dropdown: Administrador / Dizimista)
    - Switch "Ativo" (.md-switch)
    - Switch "Dizimista" (.md-switch)
    - Campo Senha (.md-text-field com toggle) — apenas no cadastro
  - Botões: "Salvar" (.md-btn--filled), "Cancelar" (.md-btn--outlined)
- [ ] Criar `static/js/pages/usuario-form.js`:
  - Se edição: GET `/api/usuarios/<id>/` e preencher form
  - Submit: validação client-side (CPF, email, campos obrigatórios) + PUT ou POST
  - Máscaras de CPF e telefone via JS (input event)
  - Redirecionar para listagem após salvar
  - Validação de CPF (algoritmo dos 2 dígitos verificadores)

### 2.4. Verificação da Fase 2

- [ ] CRUD completo de usuários funcionando via API (testar com curl/Postman)
- [ ] Listagem de usuários com busca, filtros e paginação
- [ ] Cadastro e edição com validações
- [ ] Máscaras de CPF e telefone funcionando
- [ ] Exclusão com confirmação

---

## Fase 3 — App de Ofertas

### 3.1. Criar app `ofertas`

- [ ] `python manage.py startapp ofertas`
- [ ] Modelo `Oferta`:
  - `valor` (DecimalField, max_digits=10, decimal_places=2)
  - `dizimista` (ForeignKey → User, related_name='ofertas')
  - `data` (DateField)
  - `tipo_pagamento` (CharField choices: dinheiro/cartao/pix)
  - `created_at`, `updated_at`
- [ ] Serializer: `OfertaSerializer` com todos os campos + `dizimista_nome` (read-only via source)
- [ ] ViewSet: `OfertaViewSet` (CRUD) com filtros por:
  - `dizimista` (query param)
  - `data__gte`, `data__lte` (range de datas)
  - `tipo_pagamento`
- [ ] Fazer migrações

### 3.2. Template de Listagem/Histórico de Ofertas

- [ ] Criar `ofertas/templates/ofertas/oferta_list.html`:
  - AppBar com título "Ofertas" + botão "Nova Oferta"
  - Filtros: dizimista (select via API), data inicial/final (date picker), tipo pagamento (select)
  - Tabela (.md-table): Data, Dizimista, Valor (formatado R$), Tipo Pagamento (com chip colorido), Ações (editar/deletar)
  - Totalizador no topo (card destacado com soma do período)
  - FAB "Nova Oferta" (mobile)
- [ ] Criar `static/js/pages/ofertas.js`:
  - `listarOfertas(params)` — GET `/api/ofertas/`, preenche tabela
  - `carregarDizimistas()` — GET `/api/usuarios/?is_dizimista=true` para preencher select de filtro
  - Filtros com debounce e re-render
  - Exclusão com confirmação
  - Atualizar totalizador conforme filtros

### 3.3. Template de Formulário de Oferta

- [ ] Criar `ofertas/templates/ofertas/oferta_form.html`:
  - AppBar com título "Nova Oferta" ou "Editar Oferta"
  - Card com formulário:
    - Select Dizimista (.md-dropdown populado via API)
    - Campo Valor (.md-text-field com type text, prefixo "R$", máscara de moeda)
    - Campo Data (.md-text-field com type date)
    - Select Tipo Pagamento (.md-dropdown: Dinheiro/Cartão/PIX)
  - Botões Salvar (.md-btn--filled) / Cancelar (.md-btn--outlined)
- [ ] Criar `static/js/pages/oferta-form.js`:
  - Carregar lista de dizimistas via API
  - Se edição: carregar dados da oferta
  - Submit: POST ou PUT conforme edição/criação
  - Máscara de moeda (formata valor em tempo real)
  - Redirecionar para listagem após salvar

### 3.4. Template de Listagem por Dizimista

- [ ] Criar `ofertas/templates/ofertas/oferta_dizimista.html`:
  - AppBar com título "Ofertas de [Nome do Dizimista]" + botão "Voltar"
  - Card com resumo do dizimista (nome, CPF, total de ofertas, última oferta)
  - Tabela de ofertas do dizimista (mesmo formato da listagem geral)
  - Gráfico simples (opcional): barras verticais com ofertas por mês (CSS puro)
- [ ] Criar `static/js/pages/oferta-dizimista.js`:
  - GET `/api/ofertas/?dizimista=<id>` — carregar ofertas
  - GET `/api/usuarios/<id>/` — dados do dizimista
  - Preencher resumo e tabela

### 3.5. Verificação da Fase 3

- [ ] CRUD de ofertas completo
- [ ] Listagem geral com filtros por data, dizimista e tipo pagamento
- [ ] Totalizador de valores no período
- [ ] Listagem individual por dizimista
- [ ] Máscara de moeda em valor

---

## Fase 4 — App de Dizimistas

### 4.1. Criar app `dizimistas`

- [ ] `python manage.py startapp dizimistas`
- [ ] Modelo: reutiliza `User` com `is_dizimista=True` (não cria modelo novo)
- [ ] Serializer: `DizimistaListSerializer` (nome, CPF, telefone, total_ofertas_mes, ultima_oferta, status)
- [ ] View: `DizimistaListView` (apenas GET) — retorna lista de usuários `is_dizimista=True` com métricas:
  - `total_ofertas_mes` — count de ofertas no mês corrente
  - `ultima_oferta_data` — data da última oferta
  - `status` — "ofertou" / "não ofertou" (baseado em ofertas no mês)

### 4.2. Template de Listagem de Dizimistas

- [ ] Criar `dizimistas/templates/dizimistas/dizimista_list.html`:
  - AppBar "Dizimistas" com filtro mês/ano (select)
  - Card de resumo: total de dizimistas, total que ofertaram no mês, total que não ofertaram
  - Lista de cards (.md-card), um por dizimista:
    - Avatar com inicial (letra do nome, círculo colorido)
    - Nome, CPF, telefone
    - Chip verde "Ofertou" ou chip vermelho "Não ofertou"
    - Valor total ofertado no mês
    - Data da última oferta
    - Botão "Ver ofertas" → link para `/ofertas/dizimista/<id>/`
- [ ] Criar `static/js/pages/dizimistas.js`:
  - `listarDizimistas(mes, ano)` — GET `/api/dizimistas/`
  - Preencher cards com status e cores
  - Filtro por mês/ano recarrega lista
  - Ordenação: quem não ofertou aparece primeiro (destacado)

### 4.3. Verificação da Fase 4

- [ ] Listagem de dizimistas com status de oferta
- [ ] Filtro por mês/ano
- [ ] Cards com indicador visual (verde/vermelho)
- [ ] Link para ofertas individuais

---

## Fase 5 — App de Configuração

### 5.1. Criar app `configapp`

- [ ] `python manage.py startapp configapp`
- [ ] Modelo `ConfiguracaoIgreja` (singleton):
  - `nome` (CharField)
  - `cnpj` (CharField)
  - `endereco` (TextField)
  - Singleton: apenas 1 registro, creado automaticamente via signal
- [ ] Modelo `UserProfile`:
  - `user` (OneToOne → User)
  - `theme_primary_color` (CharField, default `#6750A4`)
  - Criar signal `post_save` para criar UserProfile automaticamente
- [ ] Serializers: `ConfiguracaoIgrejaSerializer`, `UserProfileSerializer`
- [ ] Views: `ConfiguracaoIgrejaView` (GET/PUT), `UserProfileView` (GET/PUT), `ChangePasswordView`

### 5.2. Template de Configuração da Igreja

- [ ] Criar `configapp/templates/configapp/igreja_config.html`:
  - AppBar "Configuração da Igreja"
  - Card com formulário:
    - Nome da igreja (.md-text-field)
    - CNPJ (.md-text-field com máscara `__.___.___/____-__`)
    - Endereço (.md-text-field multiline)
  - Botão "Salvar" (.md-btn--filled)
- [ ] Criar `static/js/pages/igreja-config.js`: carregar dados via GET, salvar via PUT

### 5.3. Template de Configuração de Tema (Acessibilidade)

- [ ] Criar `configapp/templates/configapp/tema_config.html`:
  - AppBar "Personalizar Tema"
  - Card com seletor de cor primária:
    - 8 cores predefinidas (roxo, azul, verde, vermelho, laranja, rosa, teal, cinza)
    - Input color picker nativo para cor personalizada
    - Preview ao vivo: card de exemplo com botões, texto e chip usando a cor selecionada
  - Indicador de contraste WCAG AA (passa/não passa)
  - Botão "Salvar" (.md-btn--filled)
  - Botão "Restaurar padrão" (.md-btn--outlined)
- [ ] Criar `static/js/pages/tema-config.js`:
  - Carregar cor atual do usuário
  - Preview ao vivo alterando variável CSS `--md-sys-color-primary`
  - Gerar automaticamente `--md-sys-color-primary-container` (tom mais claro)
  - Calcular contraste com branco/preto para `--md-sys-color-on-primary`
  - Salvar via PUT `/api/configuracao/tema/`

### 5.4. Template de Dados Pessoais

- [ ] Criar `configapp/templates/configapp/profile.html`:
  - AppBar "Meus Dados"
  - Card com campos: nome, CPF (read-only), telefone, e-mail (read-only)
  - Botão "Salvar"
- [ ] Criar `static/js/pages/profile.js`:
  - GET `/api/auth/profile/`, preencher form
  - PUT para salvar alterações (apenas telefone e nome)

### 5.5. Template de Alteração de Senha

- [ ] Criar `configapp/templates/configapp/change_password.html`:
  - AppBar "Alterar Senha"
  - Card: senha atual, nova senha, confirmar nova senha
  - Validação client-side: mínimo 8 caracteres, nova senha = confirmação
  - Botão "Alterar" (.md-btn--filled)
- [ ] Criar `static/js/pages/change-password.js`: POST `/api/auth/change-password/`

### 5.6. Verificação da Fase 5

- [ ] Configuração da igreja salva e carregada
- [ ] Tema com cor personalizável, preview ao vivo e contraste verificado
- [ ] Dados pessoais editáveis
- [ ] Alteração de senha funcional

---

## Fase 6 — Responsividade e Polimento

### 6.1. Ajustes de Responsividade

- [ ] Testar todas as telas nos 3 breakpoints (≥1024px, 768–1023px, <768px)
- [ ] Sidebar: testar colapso para mini-sidebar (ícones + tooltip) em tablet
- [ ] BottomNav: testar 5 itens com ícones + labels em mobile
- [ ] Tabelas: em mobile, converter para cards (.md-card por linha)
- [ ] Formulários: adaptar grid para 1 coluna em mobile
- [ ] FAB: posicionar corretamente sobre bottom-nav em mobile
- [ ] Ajustar touch targets (mínimo 44x44px, recomendado 48x48px)
- [ ] Testar orientação paisagem/retrato em mobile

### 6.2. Animações e Transições

- [ ] Implementar `.md-ripple` via JS: no `mousedown`, criar elemento bolha que se expande e some
- [ ] Transição de páginas: fade de 200ms entre carregamentos de templates
- [ ] Hover em cards: elevação aumenta suavemente (transition)
- [ ] Snackbar: animação de entrada (slide up) e saída (fade out)
- [ ] Dialog: animação de escala + overlay fade
- [ ] BottomNav: transição de ícone ativo (preenchido/outlined)

### 6.3. Componentes Globais

- [ ] Garantir que `mdSnackbar` seja chamada em todas as operações CRUD (sucesso/erro)
- [ ] Garantir que `mdDialog` seja usada em todas as exclusões
- [ ] Adicionar `md-progress` (barra de carregamento linear no topo da página) durante requisições AJAX
- [ ] Estados vazios: ilustração + mensagem "Nenhum registro encontrado" quando lista vazia
- [ ] Estados de erro: mensagem amigável + botão "Tentar novamente"

### 6.4. Verificação da Fase 6

- [ ] Todas as telas funcionam em 320px, 768px, 1024px (viewport emulado)
- [ ] Ripple visível em todos os botões clicáveis
- [ ] Snackbar aparece em operações CRUD
- [ ] Diálogo de confirmação aparece em exclusões
- [ ] Barra de progresso visível durante requisições
- [ ] Estados vazios e de erro tratados

---

## Fase 7 — Finalização

### 7.1. Seed de Dados

- [ ] Criar `accounts/management/commands/seed_data.py`:
  - 1 administrador (admin@igreja.com / 123456)
  - 15 dizimistas com dados variados
  - 50+ ofertas em diferentes meses e tipos de pagamento
  - 1 configuração de igreja (nome, CNPJ, endereço)
- [ ] Testar `python manage.py seed_data`

### 7.2. Validações e Segurança

- [ ] Views da API protegidas com `permission_classes = [IsAuthenticated]`
- [ ] Usuário admin tem acesso a todos os endpoints
- [ ] Usuário dizimista vê apenas seus próprios dados (implementar `get_queryset` com base no user)
- [ ] CSRF: garantir que requests POST/PUT/DELETE de templates Django passem CSRF token (ou usar JWT exclusivamente)
- [ ] Sanitização de inputs nos serializers
- [ ] Tratamento de erros 403, 404 com páginas amigáveis

### 7.3. Testes Finais

- [ ] Fluxo completo: login → cadastrar usuário → cadastrar oferta → ver dizimistas → configurar tema
- [ ] Logout e login com outro perfil
- [ ] Testar alteração de senha
- [ ] Testar responsividade em dispositivo real (ou emulação)
- [ ] Verificar que todas as dependências estão no `requirements.txt`
- [ ] Verificar que `python manage.py runserver` sobe sem warnings

### 7.4. Documentação

- [ ] Atualizar `README.md` (ou criar se não existir):
  - Descrição do projeto
  - Como instalar e rodar ( `pip install -r requirements.txt` + `python manage.py migrate` + `python manage.py seed_data` )
  - Credenciais do seed
  - Estrutura do projeto
  - Tecnologias utilizadas

### 7.5. Checklist de Entrega

- [x] Tela de login funcional
- [x] CRUD de usuários (admin + dizimistas)
- [x] Listagem de dizimistas com status de oferta
- [x] CRUD de ofertas com histórico geral e individual
- [x] Configuração da igreja
- [x] Alteração de senha e dados pessoais
- [x] Acessibilidade: tema com cor personalizável
- [x] Design responsivo (desktop, tablet, celular)
- [x] Interface Flutter/Material Design 3 consistente

---

## Convenções de Código

- **Python**: PEP 8, nomes em snake_case
- **CSS**: classes no padrão BEM adaptado: `.md-componente`, `.md-componente--modificador`, `.md-componente__elemento`
- **JavaScript**: camelCase, `const`/`let`, funções descritivas
- **Templates Django**: `snake_case` para blocos e arquivos
- **Commits**: mensagens em português, formato imperativo: "Adiciona tela de login" / "Corrige validação de CPF"

---

## Estrutura Final de Arquivos (visão geral)

```
oferte/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── db.sqlite3
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── management/commands/seed_data.py
│   └── templates/accounts/
│       ├── login.html
│       ├── usuario_list.html
│       └── usuario_form.html
├── ofertas/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── templates/ofertas/
│       ├── oferta_list.html
│       ├── oferta_form.html
│       └── oferta_dizimista.html
├── dizimistas/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── templates/dizimistas/
│       └── dizimista_list.html
├── configapp/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── templates/configapp/
│       ├── igreja_config.html
│       ├── tema_config.html
│       ├── profile.html
│       └── change_password.html
├── templates/
│   └── base.html
└── static/
    ├── css/
    │   ├── material-theme.css
    │   ├── components.css
    │   └── responsive.css
    ├── js/
    │   ├── api.js
    │   ├── theme.js
    │   ├── components.js
    │   └── pages/
    │       ├── login.js
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
