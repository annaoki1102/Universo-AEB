# Documentacao de Arquitetura - Universo AEB

## Indice

1. [Visao Geral](#visao-geral)
2. [Stack Tecnologico](#stack-tecnologico)
3. [Estrutura de Pastas](#estrutura-de-pastas)
4. [Componentes Principais](#componentes-principais)
5. [Padrao de Arquitetura](#padrao-de-arquitetura)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Guia de Desenvolvimento](#guia-de-desenvolvimento)
8. [Padroes de Codigo](#padroes-de-codigo)
9. [Como Contribuir](#como-contribuir)

---

## Visao Geral

**Universo AEB** e uma plataforma web educacional da Turma AEB (Agencia Espacial Brasileira - AEB Escola). O projeto foi prototipado no Figma e convertido em uma Single Page Application (SPA) com React, TypeScript e Vite, deployada na Vercel.

A aplicacao apresenta assistentes virtuais de IA (Cosminho, Luana e Sagi-Crab) que guiam os usuarios em uma jornada de aprendizagem sobre exploracao espacial, com animacoes imersivas e tema espacial.

### Caracteristicas Principais
- **Single Page Application (SPA)** - Navegacao rapida client-side com React Router
- **Design Responsivo** - Adaptavel a todos os dispositivos (mobile-first)
- **Componentes Reutilizaveis** - Baseado em Radix UI (shadcn/ui) com ~48 componentes
- **Animacoes Fluidas** - Framer Motion para transicoes e efeitos visuais
- **Background Interativo** - Campo estelar animado via Canvas API
- **Totalmente Tipado** - TypeScript em todo o projeto
- **Deploy Automatizado** - CI/CD via Vercel

---

## Stack Tecnologico

Consulte a tabela completa de tecnologias no [README.md](./README.md#stack-tecnologica).

### Dependencias Chave e Seus Papeis

| Categoria | Pacote | Uso no Projeto |
|-----------|--------|----------------|
| **Core** | `react` 18.3.1 | Renderizacao de componentes |
| **Core** | `react-router-dom` ^7.13.2 | Rotas `/` e `/assistentes` |
| **Animacao** | `motion` 12.23.24 | Transicoes de entrada, hover e scroll em Hero, About, Features, Crew |
| **Icones** | `lucide-react` 0.487.0 | Icones em About (Rocket, Brain, Satellite) e Crew (Sparkles, Satellite, Wrench) |
| **UI** | `@radix-ui/*` | Primitivos acessiveis usados pelos componentes `src/app/components/ui/` |
| **UI** | `@mui/material` 7.3.5 | Usado no sub-projeto `vite-project/` (tela Assistentes) |
| **CSS** | `tailwindcss` 4.1.12 | Estilizacao via classes utilitarias (plugin Vite) |
| **CSS** | `tailwind-merge` 3.2.0 | Merge inteligente de classes Tailwind no `utils.ts` |
| **Notificacoes** | `sonner` 2.0.3 | Toast notifications |
| **Build** | `vite` 6.3.5 | Bundler, dev server, HMR |

---

## Estrutura de Pastas

Consulte a arvore completa no [README.md](./README.md#estrutura-do-projeto). Abaixo, o foco e na organizacao logica.

### Organizacao por Camada

| Camada | Diretorio | Responsabilidade |
|--------|-----------|------------------|
| **Entrada** | `src/main.tsx` | Monta `<BrowserRouter>` + `<App />` em `#root` |
| **Rotas** | `src/app/App.tsx` | Define rotas `/` e `/assistentes` |
| **Secoes da Home** | `src/app/components/` | Hero, About, Features, Crew, Footer, Navigation |
| **Infraestrutura UI** | `src/app/components/ui/` | ~48 componentes shadcn/ui reutilizaveis |
| **Paginas** | `src/pages/` | `Assistentes.tsx` (importa do sub-projeto `vite-project/`) |
| **Estilos** | `src/styles/` | Tailwind v4, tema customizado, fontes |
| **Assets** | `src/assets/` + `public/images/` | Imagens importadas pelo bundler e servidas estaticamente |
| **Sub-projeto** | `vite-project/` | App separado para a tela de Assistentes (React + MUI) |

---

## Componentes Principais

### Hierarquia de Renderizacao

```
main.tsx
└── <BrowserRouter>
    └── <App>
        ├── <ScrollToSection />           # Utilitario: reage ao hash da URL
        ├── <StarField />                 # Canvas fixo com 600 estrelas animadas
        ├── <Navigation />                # Nav fixa no topo (scroll-aware)
        ├── <main>
        │   ├── Route "/"
        │   │   ├── <Hero />              # CTA + imagem Sagi-Crab com glow
        │   │   ├── <About />             # 3 cards (Rocket, Brain, Satellite)
        │   │   ├── <Features />          # Grid de 3 recursos com imagens
        │   │   └── <Crew />              # Cards dos 3 assistentes
        │   └── Route "/assistentes"
        │       └── <Assistentes />       # Importa TelaAssistentes do vite-project
        └── <Footer />                    # Links de navegacao + copyright
```

### Detalhamento dos Componentes

| Componente | Arquivo | Descricao | Estado / Props |
|-----------|---------|-----------|----------------|
| **Hero** | `Hero.tsx` | Secao inicial com animacoes de entrada (opacity, x, scale), badge "Versao Alpha 1.0", CTAs "Iniciar Exploracao" e "Saiba Mais", imagem Sagi-Crab flutuante | Sem props, sem estado |
| **Navigation** | `Navigation.tsx` | Barra fixa no topo. Muda estilo ao scroll (>50px). Navegacao por secoes via `handleSectionNavigation` com scroll suave. Redireciona para `/#section` se estiver em `/assistentes` | Estado: `scrolled` (boolean) |
| **About** | `About.tsx` | Tres cards com icones Lucide (Rocket, Brain, Satellite) e animacoes whileInView | Sem props, sem estado |
| **Features** | `Features.tsx` | Grid de 3 recursos com imagens de `/public/images/`. Dados definidos em array `features` | Sem props, sem estado |
| **Crew** | `Crew.tsx` | Cards dos assistentes (Cosminho, Luana, Sagi-Crab) com icones e gradientes. Dados definidos em array `crewMembers` | Sem props, sem estado |
| **Footer** | `Footer.tsx` | Rodape com 3 colunas: branding Sagi-Crab, links de navegacao (scroll suave), info AEB Escola. Copyright 2026 | Sem props |
| **StarField** | `StarField.tsx` | Canvas full-screen fixo com 600 estrelas. Tres niveis de brilho/tamanho para profundidade. Efeito twinkle via animacao `requestAnimationFrame`. Redimensiona com a janela | Sem props, ref ao canvas |
| **ScrollToSection** | `ScrollToSection.tsx` | Componente utilitario (renderiza `null`). Observa `location.hash` e faz scroll suave para o elemento correspondente com delay de 200ms | Sem props |
| **ImageWithFallback** | `figma/ImageWithFallback.tsx` | Wrapper de `<img>` que exibe placeholder SVG em caso de erro de carregamento | Props: `React.ImgHTMLAttributes` |

---

## Padrao de Arquitetura

### Arquitetura em Camadas

```
Roteamento (React Router)
    └── Paginas / Layout (App.tsx)
        └── Componentes de Secao (Hero, About, Features, Crew)
            ├── Componentes UI (shadcn/ui, Radix UI)
            ├── Animacoes (Framer Motion)
            └── Estilos (Tailwind CSS + theme.css)
```

### Padroes de Design Utilizados

#### 1. Component-Based Architecture
Cada secao da pagina e um componente React independente. Todos exportam funcoes nomeadas (named exports), exceto `Assistentes.tsx` que usa default export:
```tsx
// src/app/components/Hero.tsx
export function Hero() {
  return (
    <section id="home" className="...">
      {/* Conteudo */}
    </section>
  );
}
```

#### 2. Utility-First CSS (Tailwind v4)
Estilos aplicados diretamente via classes. O projeto usa Tailwind v4 com o plugin `@tailwindcss/vite` (nao precisa de configuracao PostCSS para Tailwind):
```tsx
<div className="flex items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-600 p-8">
```

#### 3. shadcn/ui Pattern
Componentes primitivos de UI em `src/app/components/ui/`. Importados via alias `@/`:
```tsx
import { Button } from "@/app/components/ui/button"
import { Card } from "@/app/components/ui/card"
```

#### 4. Dados como Constantes Inline
Os componentes Features e Crew definem seus dados como arrays constantes no topo do arquivo, sem backend ou API:
```tsx
const crewMembers = [
  { name: 'Cosminho', role: 'Guia de Iniciacao Espacial', ... },
  { name: 'Luana', role: 'Especialista em Tecnologia', ... },
  { name: 'Sagi-Crab', role: 'Assistente Inteligente', ... },
];
```

#### 5. Sub-projeto Embarcado
A pagina `/assistentes` importa diretamente de `vite-project/src/App.jsx`, um projeto React separado com seu proprio `package.json` e configuracao. Isso permite desenvolvimento independente da tela de assistentes.

---

## Fluxo de Dados

### Ciclo de Vida da Aplicacao

```
1. Browser carrega index.html
        |
2. main.tsx monta <BrowserRouter> + <App /> em #root
        |
3. React Router resolve a rota ativa
        |
4. App.tsx renderiza componentes globais (StarField, Navigation, Footer)
   + componentes da rota ativa (Hero+About+Features+Crew ou Assistentes)
        |
5. Framer Motion executa animacoes de entrada (initial -> animate)
        |
6. StarField inicia loop de animacao via requestAnimationFrame
        |
7. Interacoes do usuario (scroll, clique) disparam handlers locais
```

### Comunicacao Entre Componentes

O projeto tem pouca comunicacao entre componentes. Cada secao e autossuficiente:

- **Navigation e Footer** usam `handleSectionNavigation()` / `handleFooterNavigation()` para scroll suave via DOM (`document.getElementById` + `scrollIntoView`)
- **ScrollToSection** observa `location.hash` via React Router e faz scroll automatico
- Nao ha estado global (Context, Redux, Zustand). Cada componente gerencia seu proprio estado local
- Dados dos assistentes e features sao constantes inline, sem fetch de API

---

## Guia de Desenvolvimento

### Setup Inicial

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desenvolvimento
npm run dev

# 3. Acessar em http://localhost:5173
```

> **Nota:** O sub-projeto `vite-project/` tem seu proprio `package.json`. Se for modificar a tela de Assistentes, rode `npm install` tambem dentro de `vite-project/`.

### Adicionando uma Nova Secao a Home

1. Crie o componente em `src/app/components/`:
```tsx
// src/app/components/MinhaSecao.tsx
import { motion } from 'motion/react';

export function MinhaSecao() {
  return (
    <section id="minha-secao" className="relative py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">
            Titulo
          </h2>
        </motion.div>
      </div>
    </section>
  );
}
```

2. Importe e adicione ao layout em `App.tsx`:
```tsx
import { MinhaSecao } from './components/MinhaSecao';

// Dentro da Route "/":
<>
  <Hero />
  <About />
  <Features />
  <MinhaSecao />  {/* Nova secao */}
  <Crew />
</>
```

3. Adicione o link na `Navigation.tsx` e no `Footer.tsx` se necessario.

### Adicionando uma Nova Pagina (Rota)

1. Crie o arquivo em `src/pages/`:
```tsx
// src/pages/MinhaNovaPage.tsx
export default function MinhaNovaPage() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Titulo</h1>
    </div>
  );
}
```

2. Adicione a rota em `App.tsx`:
```tsx
import MinhaNovaPage from '../pages/MinhaNovaPage';

<Routes>
  <Route path="/" element={...} />
  <Route path="/assistentes" element={<Assistentes />} />
  <Route path="/minha-pagina" element={<MinhaNovaPage />} />
</Routes>
```

> **Nota sobre SPA:** O `vercel.json` ja redireciona todas as rotas para `/`, entao novas rotas funcionam automaticamente na Vercel.

---

## Padroes de Codigo

### Convencoes do Projeto

| Aspecto | Convencao | Exemplo |
|---------|-----------|----------|
| **Arquivos de componente** | PascalCase | `Hero.tsx`, `Navigation.tsx` |
| **Arquivos utilitarios** | camelCase | `utils.ts`, `use-mobile.ts` |
| **Componentes UI (shadcn)** | kebab-case | `hover-card.tsx`, `dropdown-menu.tsx` |
| **Exports de secao** | Named export (funcao) | `export function Hero() {}` |
| **Exports de pagina** | Default export | `export default function Assistentes() {}` |
| **Animacoes** | `motion` de `motion/react` | **Nao** `framer-motion` diretamente |
| **Alias de import** | `@/` aponta para `src/` | `import { Button } from '@/app/components/ui/button'` |

### Ordem de Imports

```tsx
import { useState, useEffect } from 'react'          // 1. React core
import { useLocation } from 'react-router-dom'       // 2. React Router
import { motion } from 'motion/react'                // 3. Bibliotecas externas
import { Rocket } from 'lucide-react'                // 4. Icones
import { Button } from '@/app/components/ui/button'  // 5. Componentes UI
import imagemLocal from '../../assets/imagem.png'    // 6. Assets
```

### Padrao de Secao

Todas as secoes da home seguem o mesmo padrao:
- `<section id="nome">` com ID para ancoragem
- Container `max-w-6xl mx-auto` para largura maxima
- Animacoes `whileInView` do Framer Motion com `viewport={{ once: true }}`
- Palette de cores: gradientes cyan-to-blue, fundo `#0a0e27` / `#0f1629`

---

## Como Contribuir

Consulte [CONTRIBUTING.md](./CONTRIBUTING.md) para o guia completo de contribuicao.

---

## Configuracao de Deploy

### Vercel

O projeto esta configurado para deploy na Vercel com:
- **Build command:** `npm run build` (gera `dist/`)
- **Rewrites:** todas as rotas redirecionam para `/` (SPA) via `vercel.json`
- **Redirect SPA:** `public/_redirects` como fallback

### Alias de Path

O Vite esta configurado com alias `@` apontando para `src/`:
```ts
// vite.config.ts
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

---

## Referencias Uteis

- [Design no Figma](https://www.figma.com/design/ovtfTVNmzU5pBUH2vltfvg/Universo-AEB)
- [React Docs](https://react.dev)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS v4](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Radix UI Primitives](https://www.radix-ui.com/docs/primitives/overview/introduction)
- [React Router](https://reactrouter.com)

### Ferramentas Recomendadas para o Editor
- **Tailwind CSS IntelliSense** - Autocomplete de classes
- **ES7+ React/Redux snippets** - Snippets para React
- **TypeScript** - Suporte nativo no VS Code

