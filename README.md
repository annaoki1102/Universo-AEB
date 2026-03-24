
# 🌌 Universo AEB

Uma experiência web moderna e imersiva desenvolvida com Vite e React. O projeto foi prototipado em Figma e convertido em uma aplicação web totalmente funcional.

## 📋 Visão Geral

Este é um código bundle para o Universo AEB, um projeto de interface web inovadora. O design original foi criado no Figma e serviu como base para esta implementação web.

- **Design Original**: [Ver no Figma](https://www.figma.com/design/ovtfTVNmzU5pBUH2vltfvg/Universo-AEB)
- **Status**: Em desenvolvimento
- **Versão**: v1.0

## 🚀 Tecnologias

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool e development server
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI / shadcn/ui** - Componentes de UI acessíveis
- **PostCSS** - Processamento de CSS

## 📦 Pré-requisitos

- Node.js 18.0 ou superior
- npm 9.0 ou superior

## ⚙️ Instalação

1. Clone ou acesse o repositório
2. Instale as dependências:

```bash
npm install
```

## 🎯 Como Rodar

### Desenvolvimento

Inicie o servidor de desenvolvimento com hot reload:

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173` (ou a porta exibida no terminal).

### Build para Produção

Crie uma build otimizada para produção:

```bash
npm run build
```

### Preview da Build

Visualize a build de produção localmente:

```bash
npm run preview
```

## 📁 Estrutura do Projeto

```
src/
├── app/
│   ├── App.tsx              # Componente principal
│   └── components/          # Componentes reutilizáveis
│       ├── About.tsx
│       ├── Crew.tsx
│       ├── Features.tsx
│       ├── Footer.tsx
│       ├── Hero.tsx
│       ├── Navigation.tsx
│       ├── ScrollToSection.tsx
│       ├── StarField.tsx
│       └── ui/              # Componentes de UI base
├── pages/                   # Páginas da aplicação
├── assets/                  # Imagens e recursos
└── styles/                  # Estilos globais
```

## 🎨 Principais Componentes

- **Hero** - Seção de introdução principal
- **Navigation** - Navegação do site
- **Features** - Destaques e funcionalidades
- **Crew** - Apresentação da equipe
- **About** - Seção sobre o projeto
- **Footer** - Rodapé
- **StarField** - Efeito visual de fundo

## 📝 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `npm run dev` | Inicia servidor de desenvolvimento |
| `npm run build` | Cria build para produção |
| `npm run preview` | Visualiza build de produção |

## 🔍 Linting

O projeto usa ESLint. Verifique a configuração em `eslint.config.js`.

## 📚 Recursos Adicionais

- [Documentação Vite](https://vitejs.dev)
- [Documentação React](https://react.dev)
- [Documentação Tailwind CSS](https://tailwindcss.com)
- [Shadcn/ui Components](https://ui.shadcn.com)

## 📄 Licença e Atribuições

Veja [ATTRIBUTIONS.md](./ATTRIBUTIONS.md) para detalhes sobre licenças e atribuições.

## 👤 Autor

Universo AEB

---

**Desenvolvido com ❤️**
  