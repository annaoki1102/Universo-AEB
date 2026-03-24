# 📐 Documentação de Arquitetura - Universo AEB

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Estrutura de Pastas](#estrutura-de-pastas)
4. [Componentes Principais](#componentes-principais)
5. [Padrão de Arquitetura](#padrão-de-arquitetura)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Guia de Desenvolvimento](#guia-de-desenvolvimento)
8. [Padrões de Código](#padrões-de-código)
9. [Como Contribuir](#como-contribuir)

---

## 🎯 Visão Geral

**Universo AEB** é uma aplicação web moderna construída com React, TypeScript e Vite. O projeto foi prototipado em Figma e convertido em uma Single Page Application (SPA) completamente funcional, implementada em Vercel.

### Características Principais
- ✅ **Single Page Application (SPA)** - Navegação rápida cliente-side
- ✅ **Design Responsivo** - Totalmente adaptável a todos os devices
- ✅ **Componentes Reutilizáveis** - Baseado em Radix UI (shadcn/ui)
- ✅ **Animações Fluidas** - Utilizando Framer Motion
- ✅ **Totalmente Tipado** - TypeScript em todo o projeto
- ✅ **Pronto para Produção** - Otimizado e deployado em Vercel

---

## 🛠️ Stack Tecnológico

### Frontend
| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **React** | 18.3.1 | Framework UI |
| **TypeScript** | 5.x | Type safety |
| **Vite** | 6.3.5 | Build tool e dev server |
| **React Router** | 7.13.2 | Roteamento SPA |

### Estilos
| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Tailwind CSS** | 4.1.12 | Utility-first CSS framework |
| **PostCSS** | 8.x | Processamento de CSS |

### Componentes & UI
| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **Radix UI** | 1.x | Componentes acessíveis primitivos |
| **shadcn/ui** | - | Componentes UI built com Radix |
| **Material UI** | 5.x | Componentes Material Design |

### Animações & Interatividade
| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **Framer Motion** | 12.23.24 | Animações React |
| **React Hook Form** | 7.55.0 | Gerenciamento de formulários |
| **React Dnd** | 16.0.1 | Drag & drop |

### Utilitários
| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **Recharts** | 2.15.2 | Gráficos e visualizações |
| **Sonner** | 2.0.3 | Toast notifications |
| **Zod** | 3.x | Validação de data/schemas |

### Deploy
| Serviço | Propósito |
|--------|----------|
| **Vercel** | Hosting, CI/CD e serverless functions |

---

## 📁 Estrutura de Pastas

```
Universo AEB/
│
├── 📂 src/                              # Código-fonte principal
│   ├── main.tsx                         # Entry point React
│   │
│   ├── 📂 app/                          # Aplicação principal
│   │   ├── App.tsx                      # Componente raiz com rotas
│   │   │
│   │   ├── 📂 components/               # Componentes reutilizáveis
│   │   │   ├── Hero.tsx                 # Seção hero com animações
│   │   │   ├── Navigation.tsx           # Barra de navegação
│   │   │   ├── About.tsx                # Seção sobre o projeto
│   │   │   ├── Features.tsx             # Funcionalidades/características
│   │   │   ├── Crew.tsx                 # Seção de assistentes/equipe
│   │   │   ├── Footer.tsx               # Rodapé
│   │   │   ├── StarField.tsx            # Background animado com estrelas
│   │   │   ├── ScrollToSection.tsx      # Scroll suave entre seções
│   │   │   │
│   │   │   ├── 📂 figma/                # Componentes adaptados do Figma
│   │   │   │   └── ImageWithFallback.tsx # Componente com fallback
│   │   │   │
│   │   │   └── 📂 ui/                   # Componentes de UI base (shadcn/ui)
│   │   │       ├── accordion.tsx         # Accordion component
│   │   │       ├── alert.tsx             # Alert component
│   │   │       ├── button.tsx            # Button component
│   │   │       ├── card.tsx              # Card component
│   │   │       ├── dialog.tsx            # Dialog/modal component
│   │   │       ├── form.tsx              # Form wrapper
│   │   │       ├── input.tsx             # Input field
│   │   │       ├── select.tsx            # Select dropdown
│   │   │       ├── tabs.tsx              # Tabs component
│   │   │       ├── table.tsx             # Table component
│   │   │       ├── dropdown-menu.tsx     # Dropdown menu
│   │   │       ├── hover-card.tsx        # Hover card
│   │   │       ├── sidebar.tsx           # Sidebar layout
│   │   │       └── [+25 mais componentes]
│   │   │
│   │   └── 📂 pages/                    # Páginas da aplicação
│   │       └── Assistentes.tsx          # Página de assistentes/IA
│   │
│   ├── 📂 assets/                       # Mídia e recursos estáticos
│   │   ├── sagicrab.png
│   │   ├── logo.png
│   │   └── [outras imagens]
│   │
│   ├── 📂 styles/                       # Estilos globais
│   │   ├── index.css                    # Arquivo principal de imports
│   │   ├── tailwind.css                 # Configuração Tailwind v4
│   │   ├── theme.css                    # Variáveis de tema customizadas
│   │   └── fonts.css                    # Importação de fontes
│   │
│   ├── vite-env.d.ts                    # Tipos Vite
│
├── 📂 public/                           # Assets servidos estaticamente
│   └── _redirects                       # Regras de redirect Vercel (SPA)
│
├── 📂 dist/                             # Build de produção (gerado)
│
├── ⚙️ index.html                         # Template HTML
├── ⚙️ vite.config.ts                     # Configuração Vite
├── ⚙️ postcss.config.mjs                 # Configuração PostCSS
├── ⚙️ package.json                       # Dependências e scripts
├── ⚙️ package-lock.json                  # Lock file
├── ⚙️ tsconfig.json                      # Configuração TypeScript
├── ⚙️ vercel.json                        # Configuração Vercel
│
├── 📄 README.md                         # Documentação principal
├── 📄 ARCHITECTURE.md                   # Este arquivo
├── 📄 ATTRIBUTIONS.md                   # Atribuições e créditos

```

### Legenda
- 📂 = Pasta/Diretório
- ⚙️ = Arquivo de configuração
- 📄 = Arquivo de documentação

---

## 🧩 Componentes Principais

### Estrutura de Layout Principal

A aplicação segue uma estrutura hierárquica bem definida:

```
<BrowserRouter>
  <App>
    <Routes>
      <Route path="/" element={<HomePage />}>
        <StarField />                    ← Background animado
        <Navigation />                   ← Barra de navegação
        <Hero />                         ← Seção destaque
        <About />                        ← Sobre o projeto
        <Features />                     ← Funcionalidades
        <Crew />                         ← Assistentes
        <Footer />                       ← Rodapé
      </Route>
      <Route path="/assistentes" element={<Assistentes />} />
    </Routes>
  </App>
</BrowserRouter>
```

### Descrição dos Componentes

#### 🎯 Hero.tsx
**Propósito**: Seção inicial chamativa com animações  
**Features**:
- Animações de entrada com Framer Motion
- Conteúdo dinâmico com CTAs (Call To Action)
- Responsivo para mobile

**Props**: Nenhum (utiliza dados internos)  
**Estilo**: Tailwind CSS com animações

#### 🧭 Navigation.tsx
**Propósito**: Barra de navegação principal  
**Features**:
- Links para seções principais
- Menu mobile responsivo
- Integração com React Router
- Scroll suave via `ScrollToSection`

**Props**: Nenhum  
**Eventos**: Navega para seções anchor

#### ℹ️ About.tsx
**Propósito**: Apresentação do projeto  
**Features**:
- Descrição textual
- Imagens e ícones
- Layout responsivo

#### ✨ Features.tsx
**Propósito**: Destaque de funcionalidades  
**Features**:
- Grid de features
- Ícones visuais
- Descrições concisas

#### 👥 Crew.tsx
**Propósito**: Apresentação dos assistentes/equipe  
**Features**:
- Cards com perfis
- Informações de cada assistente
- Layout em grid

#### 🔖 Footer.tsx
**Propósito**: Rodapé com informações e links  
**Features**:
- Links rápidos
- Informações de contato
- Copyright

#### ⭐ StarField.tsx
**Propósito**: Background animado com efeito de campo estelar  
**Features**:
- Canvas animado
- Efeito parallax
- Performance otimizada

#### 📜 ScrollToSection.tsx
**Propósito**: Gerencia scroll suave entre seções  
**Features**:
- Scroll animation
- Ancoras de navegação
- Integração com Navigation

---

## 🏗️ Padrão de Arquitetura

### Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│    User Interface Layer             │
│  (Componentes React, UI shadcn)    │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Component Logic Layer              │
│  (State, Handlers, Effects)         │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Styling Layer                      │
│  (Tailwind CSS, theme.css)          │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│  Routing Layer                      │
│  (React Router)                     │
└─────────────────────────────────────┘
```

### Padrões de Design Utilizados

#### 1. **Component-Based Architecture**
Cada seção é um componente React independente e reutilizável:
```tsx
// Exemplo: src/app/components/Hero.tsx
function Hero() {
  return (
    <section className="hero" id="hero">
      {/* Conteúdo */}
    </section>
  );
}
```

#### 2. **Utility-First CSS (Tailwind)**
Estilos aplicados diretamente via classes:
```tsx
<div className="flex items-center justify-center bg-gradient-to-r from-purple-500 to-pink-500 p-8">
```

#### 3. **shadcn/ui Pattern**
Componentes primitivos de UI importados e customizáveis:
```tsx
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

export function MyComponent() {
  return (
    <Card>
      <Button>Click me</Button>
    </Card>
  )
}
```

#### 4. **SPA (Single Page Application)**
Toda navegação acontece lado-cliente via React Router:
```tsx
// Em App.tsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/assistentes" element={<Assistentes />} />
  </Routes>
</BrowserRouter>
```

---

## 🔄 Fluxo de Dados

### Ciclo de Vida da Aplicação

```
1. Browser carrega index.html
        ↓
2. main.tsx monta React em #root
        ↓
3. <BrowserRouter> inicializa routing
        ↓
4. <App /> renderiza com rotas ativas
        ↓
5. Componentes renderizam conforme rota
        ↓
6. Interações disparam handlers
        ↓
7. Estado atualiza (se aplicável)
        ↓
8. Re-render de componentes afetados
```

### Fluxo de Dados Entre Componentes

```
App (raiz)
├── Route / (Home)
│   ├── StarField [background]
│   ├── Navigation
│   │   └── Scroll → ScrollToSection
│   ├── Hero
│   ├── About
│   ├── Features
│   ├── Crew
│   └── Footer
└── Route /assistentes
    └── Assistentes
        └── Footer
```

**Comunicação**: Props para baixo, callbacks para cima (padrão React)

---

## 🚀 Guia de Desenvolvimento

### Setup Inicial

```bash
# 1. Instalar dependências
npm install

# 2. Iniciar servidor de desenvolvimento
npm run dev

# 3. Acessar em http://localhost:5173
```

### Adicionando um Novo Componente

#### 1. Criar arquivo do componente
```tsx
// src/app/components/MeuComponente.tsx
import { FC } from 'react'

interface MeuComponenteProps {
  titulo: string
  descricao?: string
}

export const MeuComponente: FC<MeuComponenteProps> = ({ 
  titulo, 
  descricao 
}) => {
  return (
    <div className="p-4 rounded-lg bg-white shadow-md">
      <h2 className="text-2xl font-bold">{titulo}</h2>
      {descricao && <p className="text-gray-600">{descricao}</p>}
    </div>
  )
}

export default MeuComponente
```

#### 2. Importar e usar em outro componente
```tsx
// src/app/components/SomeSection.tsx
import MeuComponente from './MeuComponente'

export function SomeSection() {
  return (
    <section>
      <MeuComponente 
        titulo="Bem-vindo" 
        descricao="Esta é uma seção nova"
      />
    </section>
  )
}
```

### Adicionando uma Nova Página

#### 1. Criar arquivo da página
```tsx
// src/pages/MinhaNovaPage.tsx
export function MinhaNovaPage() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Minha Nova Página</h1>
    </div>
  )
}
```

#### 2. Adicionar rota em App.tsx
```tsx
// src/app/App.tsx
import { MinhaNovaPage } from '@/pages/MinhaNovaPage'

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={/* ... */} />
        <Route path="/minha-pagina" element={<MinhaNovaPage />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### Adicionando um Componente de UI Customizado

Se for usar um componente UI shadcn que ainda não existe:

```bash
# Exemplo: adicionar um tooltip
npx shadcn-ui@latest add tooltip
```

Isso cria `src/components/ui/tooltip.tsx` com o componente pronto.

---

## 📝 Padrões de Código

### 1. **Nomeação de Arquivos**
- Componentes: PascalCase (ex: `Hero.tsx`, `Navigation.tsx`)
- Utilidades: camelCase (ex: `utils.ts`, `hooks.ts`)
- Páginas: PascalCase (ex: `Assistentes.tsx`)

### 2. **Estrutura de Componentes**

```tsx
// ✅ PADRÃO RECOMENDADO
import { FC, useState } from 'react'
import { Button } from '@/components/ui/button'

interface MyComponentProps {
  title: string
  onClose?: () => void
}

/**
 * MyComponent - Descrição breve do componente
 * @param title - Título do componente
 * @param onClose - Callback quando fechar
 */
export const MyComponent: FC<MyComponentProps> = ({ 
  title, 
  onClose 
}) => {
  const [count, setCount] = useState(0)

  const handleIncrement = () => setCount(c => c + 1)

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-bold">{title}</h2>
      <p>Count: {count}</p>
      <Button onClick={handleIncrement}>Increment</Button>
      {onClose && <Button onClick={onClose}>Close</Button>}
    </div>
  )
}
```

### 3. **Estilização com Tailwind**

```tsx
// ✅ BOM - Classes bem organizadas
<div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg hover:shadow-xl transition-shadow">
  {/* conteúdo */}
</div>

// ❌ EVITAR - Classes desorganizadas
<div className="p-4 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-between rounded-lg shadow-lg hover:shadow-xl transition-shadow">

// Usar variáveis para classes repetidas
const buttonClass = "px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
```

### 4. **Imports Organizados**

```tsx
// ✅ ORDEM RECOMENDADA
import { FC, useState, useEffect } from 'react'          // React core
import { useNavigate } from 'react-router-dom'          // Router
import { motion } from 'framer-motion'                  // Libraries
import { Button } from '@/components/ui/button'         // UI Components
import { MyHelper } from '@/utils/helpers'              // Utils
import './MyComponent.css'                              // Styles
```

### 5. **Tipos e Interfaces**

```tsx
// ✅ BEM TIPADO
interface UserProfile {
  id: string
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'
  createdAt: Date
}

interface CardProps {
  user: UserProfile
  onClick?: (id: string) => void
}

export const UserCard: FC<CardProps> = ({ user, onClick }) => {
  // Implementation
}

// ❌ EVITAR
const UserCard = (props: any) => {
  // Implementation
}
```

---

## 🤝 Como Contribuir

### Passo a Passo

#### 1. **Clonar/Preparar Ambiente**
```bash
git clone <repo>
cd "Universo AEB"
npm install
npm run dev
```

#### 2. **Criar uma Feature**
```bash
git checkout -b feature/nome-da-feature
```

#### 3. **Fazer Mudanças**
- Seguir os padrões de código documentados acima
- Atualizar componentes conforme necessário
- Testar no dev server

#### 4. **Commit**
```bash
git add .
git commit -m "feat: descrição da feature"
```

#### 5. **Push**
```bash
git push origin feature/nome-da-feature
```

### Convenção de Commits
Usar [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova feature
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação (sem mudança de funcionalidade)
- `refactor:` Refatoração de código
- `test:` Testes
- `chore:` Dependências, build, etc.

Exemplos:
```bash
git commit -m "feat: adicionar componente de busca"
git commit -m "fix: corrigir animação do Hero"
git commit -m "docs: atualizar README"
```

### Checklist Antes de Submeter

- [ ] Código segue os padrões do projeto
- [ ] TypeScript sem erros (`npm run build`)
- [ ] Componentes são reutilizáveis
- [ ] Props são bem tipadas
- [ ] Responsivo em mobile
- [ ] Sem console.log de debug
- [ ] Issues/TODOs documentados

---

## 📚 Referências Úteis

### Documentações
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Radix UI Primitives](https://www.radix-ui.com/docs/primitives/overview/introduction)
- [shadcn/ui Components](https://ui.shadcn.com)
- [React Router](https://reactrouter.com/en/main)
- [Framer Motion](https://www.framer.com/motion/)

### Ferramentas Recomendadas
- **VS Code** - Editor recomendado
- **ES7+ React/Redux/React-Native snippets** - Extensão útil
- **Tailwind CSS IntelliSense** - Autocomplete CSS
- **TypeScript Vue Plugin** - Para melhor TypeScript support

### Figma
- [Design Original - Universo AEB](https://www.figma.com/design/ovtfTVNmzU5pBUH2vltfvg/Universo-AEB)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar documentação acima
2. Buscar nos arquivos do projeto
3. Consultar as dependências na seção Stack Tecnológico
4. Verificar issues no repositório Git

---

**Última atualização**: Março 2026  
**Status**: Ativo e em desenvolvimento  
**Deploy**: Vercel

