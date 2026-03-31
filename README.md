# Universo AEB

Plataforma web educacional da **Turma AEB** (Agencia Espacial Brasileira - AEB Escola), com tema espacial imersivo. O projeto apresenta assistentes virtuais de IA que guiam os usuarios em uma jornada de aprendizagem sobre exploracao espacial, satelites e tecnologia.

Prototipado no Figma e convertido em uma Single Page Application totalmente funcional, hospedada na Vercel.

| | |
|---|---|
| **Design Original** | [Ver no Figma](https://www.figma.com/design/ovtfTVNmzU5pBUH2vltfvg/Universo-AEB) |
| **Deploy** | [Vercel](https://vercel.com) |
| **Status** | Em desenvolvimento (Alpha 1.0) |

---

## Stack Tecnologica

| Categoria | Tecnologia | Versao | Descricao |
|-----------|-----------|--------|-----------|
| **Framework** | React | 18.3.1 | Biblioteca de UI |
| **Linguagem** | TypeScript | 5.x | Tipagem estatica |
| **Build** | Vite | 6.3.5 | Bundler e dev server |
| **Estilos** | Tailwind CSS | 4.1.12 | Framework CSS utility-first |
| **Componentes UI** | shadcn/ui (Radix UI) | - | Primitivos acessiveis |
| **Componentes UI** | Material UI | 5.x | Componentes Material Design |
| **Animacoes** | Framer Motion | 12.23.24 | Animacoes declarativas em React |
| **Roteamento** | React Router | 7.13.2 | Navegacao SPA |
| **Formularios** | React Hook Form | 7.55.0 | Gerenciamento de formularios |
| **Graficos** | Recharts | 2.15.2 | Visualizacoes de dados |
| **Validacao** | Zod | 3.x | Validacao de schemas |
| **Deploy** | Vercel | - | Hosting e CI/CD |

---

## Pre-requisitos

- **Node.js** 18.0 ou superior
- **npm** 9.0 ou superior

---

## Inicio Rapido

```bash
# 1. Clone o repositorio
git clone https://github.com/annaoki1102/Universo-AEB.git
cd Universo-AEB

# 2. Instale as dependencias
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

A aplicacao estara disponivel em `http://localhost:5173`.

### Scripts Disponiveis

| Script | Descricao |
|--------|-----------|
| `npm run dev` | Inicia o servidor de desenvolvimento com hot reload |
| `npm run build` | Gera a build otimizada para producao em `dist/` |
| `npm run preview` | Serve a build de producao localmente para preview |

---

## Estrutura do Projeto

```
Universo-AEB/
├── src/
│   ├── main.tsx                        # Ponto de entrada (monta React + BrowserRouter)
│   ├── vite-env.d.ts                   # Tipos do Vite
│   │
│   ├── app/
│   │   ├── App.tsx                     # Componente raiz com rotas
│   │   └── components/
│   │       ├── Hero.tsx                # Secao hero com animacoes Framer Motion
│   │       ├── Navigation.tsx          # Barra de navegacao fixa com scroll suave
│   │       ├── About.tsx               # Secao sobre o projeto (cards com icones)
│   │       ├── Features.tsx            # Grid de recursos com imagens
│   │       ├── Crew.tsx                # Apresentacao dos assistentes virtuais
│   │       ├── Footer.tsx              # Rodape com links de navegacao
│   │       ├── StarField.tsx           # Background animado com campo estelar (Canvas)
│   │       ├── ScrollToSection.tsx     # Gerencia scroll suave via hash da URL
│   │       ├── figma/
│   │       │   └── ImageWithFallback.tsx  # Imagem com fallback em caso de erro
│   │       └── ui/                     # ~48 componentes shadcn/ui (button, card, dialog...)
│   │
│   ├── pages/
│   │   └── Assistentes.tsx             # Pagina dos assistentes de IA
│   │
│   ├── assets/                         # Imagens importadas pelo bundler
│   │   ├── sagicrab.png
│   │   └── ...
│   │
│   └── styles/
│       ├── index.css                   # Arquivo principal (importa os demais)
│       ├── tailwind.css                # Configuracao Tailwind v4
│       ├── theme.css                   # Variaveis de tema (light/dark)
│       └── fonts.css                   # Importacao de fontes
│
├── public/
│   ├── images/                         # Imagens servidas estaticamente
│   │   ├── ia.png
│   │   ├── navegacao.png
│   │   └── satelite.png
│   └── _redirects                      # Regras de redirect para SPA
│
├── vite-project/                       # Sub-projeto Vite (tela de Assistentes)
│
├── index.html                          # Template HTML principal
├── vite.config.ts                      # Configuracao Vite (React + Tailwind + alias @)
├── postcss.config.mjs                  # Configuracao PostCSS
├── vercel.json                         # Configuracao de rewrites para SPA na Vercel
├── package.json                        # Dependencias e scripts
└── package-lock.json                   # Lock file
```

---

## Rotas da Aplicacao

| Rota | Componente | Descricao |
|------|-----------|-----------|
| `/` | Home (Hero + About + Features + Crew) | Pagina principal com todas as secoes |
| `/assistentes` | `Assistentes.tsx` | Pagina dedicada aos assistentes de IA |

A navegacao entre secoes na pagina principal usa ancoras com scroll suave (`/#home`, `/#about`, `/#features`, `/#crew`).

---

## Assistentes Virtuais (Tripulacao)

O projeto apresenta tres assistentes virtuais com personalidades distintas:

| Assistente | Funcao | Descricao |
|-----------|--------|-----------|
| **Cosminho** | Guia de Iniciacao Espacial | Orienta novos exploradores nos fundamentos da navegacao espacial |
| **Luana** | Especialista em Tecnologia e Satelites | Responsavel pela rede de satelites e monitoramento |
| **Sagi-Crab** | Assistente Inteligente (em construcao) | IA adaptativa para suporte em exploracao espacial |

---

## Arquitetura

Para detalhes sobre a arquitetura do projeto, padroes de design, fluxo de dados e guias de desenvolvimento, consulte [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Como Contribuir

1. Faca um fork ou clone do repositorio
2. Crie uma branch para sua feature: `git checkout -b feature/nome-da-feature`
3. Faca commit com [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m "feat: descricao"`
4. Faca push e abra um Pull Request

Para mais detalhes, consulte [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Licenca e Atribuicoes

Veja [ATTRIBUTIONS.md](./ATTRIBUTIONS.md) para detalhes sobre licencas de bibliotecas e recursos utilizados.

---

## Links Uteis

- [Documentacao React](https://react.dev)
- [Documentacao Vite](https://vitejs.dev)
- [Documentacao Tailwind CSS](https://tailwindcss.com)
- [Componentes shadcn/ui](https://ui.shadcn.com)
- [Framer Motion](https://www.framer.com/motion/)
- [React Router](https://reactrouter.com)
  