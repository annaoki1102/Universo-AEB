# Guia de Contribuicao

Obrigado por considerar contribuir com o Universo AEB! Este guia explica como configurar o ambiente, fazer alteracoes e enviar suas contribuicoes.

---

## Pre-requisitos

- **Node.js** 18.0 ou superior
- **npm** 9.0 ou superior
- **Git**

---

## Setup do Ambiente

```bash
# 1. Fork e clone o repositorio
git clone https://github.com/SEU-USUARIO/Universo-AEB.git
cd Universo-AEB

# 2. Instale as dependencias
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev

# 4. Acesse http://localhost:5173
```

### Sub-projeto Assistentes

Se for trabalhar na pagina de Assistentes (`/assistentes`), instale as dependencias do sub-projeto tambem:

```bash
cd vite-project
npm install
cd ..
```

---

## Fluxo de Trabalho

### 1. Crie uma branch

```bash
git checkout -b feature/nome-da-feature
```

Use prefixos descritivos:
- `feature/` para novas funcionalidades
- `fix/` para correcoes de bugs
- `docs/` para documentacao
- `refactor/` para refatoracoes

### 2. Faca suas alteracoes

- Siga os [padroes de codigo](./ARCHITECTURE.md#padroes-de-codigo) documentados
- Teste no servidor de desenvolvimento (`npm run dev`)
- Verifique a responsividade em diferentes tamanhos de tela

### 3. Verifique o build

Antes de commitar, garanta que o TypeScript compila sem erros:

```bash
npm run build
```

### 4. Faca commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add <arquivos-modificados>
git commit -m "tipo: descricao curta"
```

#### Tipos de Commit

| Tipo | Descricao | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat: adicionar secao de contato` |
| `fix` | Correcao de bug | `fix: corrigir scroll no mobile` |
| `docs` | Documentacao | `docs: atualizar README` |
| `style` | Formatacao (sem mudanca funcional) | `style: ajustar espacamento do footer` |
| `refactor` | Refatoracao de codigo | `refactor: simplificar logica do StarField` |
| `chore` | Dependencias, build, config | `chore: atualizar tailwindcss` |

### 5. Envie e abra um PR

```bash
git push origin feature/nome-da-feature
```

Abra um Pull Request no GitHub com uma descricao clara das alteracoes.

---

## Checklist Antes de Enviar

- [ ] O codigo segue os padroes do projeto
- [ ] `npm run build` executa sem erros
- [ ] Componentes sao responsivos (testar em mobile e desktop)
- [ ] Props estao tipadas com TypeScript
- [ ] Nenhum `console.log` de debug restante
- [ ] Animacoes usam `motion` de `motion/react` (nao `framer-motion` diretamente)
- [ ] Imports seguem a [ordem recomendada](./ARCHITECTURE.md#ordem-de-imports)

---

## Estrutura de um Novo Componente

Ao criar um componente de secao, siga o padrao existente:

```tsx
// src/app/components/NomeDoComponente.tsx
import { motion } from 'motion/react';

export function NomeDoComponente() {
  return (
    <section id="nome-da-secao" className="relative py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">
            Titulo da Secao
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Descricao da secao
          </p>
        </motion.div>
      </div>
    </section>
  );
}
```

### Pontos importantes:
- Use `id` na `<section>` para ancoragem de navegacao
- Container `max-w-6xl mx-auto` para consistencia de largura
- Animacoes `whileInView` com `viewport={{ once: true }}` para animar apenas uma vez
- Palette de cores: gradientes cyan-to-blue, fundos `#0a0e27` / `#0f1629`
- Named export (`export function`) para componentes de secao

---

## Duvidas?

Verifique a [documentacao de arquitetura](./ARCHITECTURE.md) para entender a estrutura do projeto em detalhes.
