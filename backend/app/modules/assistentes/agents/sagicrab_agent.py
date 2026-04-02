"""
SagiCrabAgent — Orquestrador da Turma AEB
Responde de forma geral usando contexto do Qdrant (todos os documentos)
e delega para Cosminho ou Luana para respostas mais específicas.
"""

from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from .utils import get_response
from copy import deepcopy
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Optional

load_dotenv()

# ✅ saudações que não precisam de busca no Qdrant
SAUDACOES = [
    "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite",
    "tudo bem", "tudo bom", "hey", "hello", "hi", "e aí", "eai",
    "como vai", "como você está", "boa", "salve",
]

# ✅ delegação garantida via Python — não depende do LLM
DELEGACAO = {
    "cosminho":  "\n\n🚀 Para mais detalhes técnicos, converse com o Cosminho! Troque de personagem no menu lateral.",
    "luana":     "\n\n⚖️ Para mais detalhes jurídicos, converse com a Luana! Troque de personagem no menu lateral.",
    "sagicrab":  "",  # domínio próprio do Sagi-Crab — sem delegação
    "misto":     "\n\n🚀 Cosminho para detalhes técnicos | ⚖️ Luana para detalhes jurídicos. Troque no menu lateral!",
    "geral":     "\n\n💬 Posso te direcionar para o Cosminho (técnico) ou a Luana (legislação). É só perguntar! 🦀",
}


class SagiCrabAgent:
    """
    Sagi-Crab — membro da Turma AEB.
    Busca em TODOS os documentos (sem filtro de agente)
    e sempre delega para o especialista certo ao final.
    """

    def __init__(self) -> None:
        self.client     = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.model_name = getenv("MODEL_NAME")

        print("   📊 Carregando embeddings (multilingual-e5-large)...")
        self.embedder = SentenceTransformer("intfloat/multilingual-e5-large")
        print("   ✅ Embeddings carregados")

        print("   📊 Carregando reranker...")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        print("   ✅ Reranker carregado")

        # Qdrant
        self.collection_name = getenv("QDRANT_COLLECTION", "aeb_documentos")
        qdrant_host    = getenv("QDRANT_HOST", "localhost")
        qdrant_port    = int(getenv("QDRANT_PORT", "6333"))
        qdrant_api_key = getenv("QDRANT_API_KEY", None)

        try:
            print(f"   🔌 Conectando ao Qdrant ({qdrant_host}:{qdrant_port})...")
            if qdrant_api_key:
                self.qdrant_client = QdrantClient(
                    url=f"https://{qdrant_host}",
                    api_key=qdrant_api_key,
                    timeout=60,
                )
            else:
                self.qdrant_client = QdrantClient(
                    host=qdrant_host,
                    port=qdrant_port,
                    timeout=60,
                )

            collections = [
                c.name for c in
                self.qdrant_client.get_collections().collections
            ]

            if self.collection_name in collections:
                self.use_qdrant = True
                print(f"   ✅ Qdrant conectado — coleção: {self.collection_name}")
            else:
                self.use_qdrant = False
                print(f"   ⚠️  Coleção '{self.collection_name}' não encontrada")

        except Exception as e:
            self.use_qdrant = False
            print(f"   ⚠️  Erro Qdrant: {e}")

        print("✅ SagiCrabAgent: ativo")

    def is_saudacao(self, text: str) -> bool:
        """Detecta se a mensagem é uma saudação simples."""
        text_lower = text.lower().strip()
        return (
            any(s in text_lower for s in SAUDACOES)
            and len(text_lower.split()) <= 5
        )

    def get_domain_from_context(self, context: str) -> str:
        """Detecta o domínio dominante nos trechos do contexto."""
        if not context:
            return "geral"
        has_cosminho  = "Domínio: cosminho"  in context
        has_luana     = "Domínio: luana"     in context
        has_sagicrab  = "Domínio: sagicrab"  in context

        # Missão Centenário é exclusiva do Sagi-Crab — sem delegação
        if has_sagicrab and not has_cosminho and not has_luana:
            return "sagicrab"
        if has_cosminho and has_luana:
            return "misto"
        elif has_luana:
            return "luana"
        elif has_cosminho:
            return "cosminho"
        return "geral"

    def search(self, query: str, top_k: int = 8) -> Optional[str]:
        """
        Busca em TODOS os documentos (sem filtro de agente).
        Aplica reranker e retorna contexto formatado.
        """
        if not self.use_qdrant:
            return None

        try:
            query_emb = self.embedder.encode(
                f"query: {query}", normalize_embeddings=True).tolist()

            results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_emb,
                limit=top_k,
                with_payload=True,
            ).points

            if not results:
                return None

            # reranker
            pairs  = [[query, r.payload["text"]] for r in results]
            scores = self.reranker.predict(pairs)
            ranked = sorted(zip(results, scores),
                            key=lambda x: x[1], reverse=True)[:5]
            results = [r for r, _ in ranked]

            # formatar contexto
            parts = []
            for i, hit in enumerate(results, 1):
                page     = hit.payload.get("page", "?")
                # ✅ corrigido — tenta doc_name e name antes do fallback
                doc_name = (hit.payload.get("doc_name")
                            or hit.payload.get("name", "AEB"))
                agent    = hit.payload.get("agent", "?")
                text     = hit.payload.get("text", "")
                score    = getattr(hit, "score", 0.0)
                parts.append(
                    f"[Trecho {i} — {doc_name} | Pág. {page} | "
                    f"Domínio: {agent} | Relevância: {score:.3f}]\n{text}"
                )

            return "\n\n" + "="*60 + "\n\n".join(parts)

        except Exception as e:
            print(f"   ⚠️  Erro na busca: {e}")
            return None

    def respond(self, messages: List[Dict],
                query_type: str = "geral") -> Dict:

        messages   = deepcopy(messages)
        user_input = messages[-1]["content"]

        # saudações simples não buscam no Qdrant
        saudacao = self.is_saudacao(user_input)

        context = None
        if self.use_qdrant and not saudacao:
            print("🦀 Sagi-Crab: buscando no Qdrant (todos os docs)...")
            context = self.search(user_input)
            if context:
                print("   ✅ Contexto obtido")
            else:
                print("   ⚠️  Nenhum contexto encontrado")
        elif saudacao:
            print("🦀 Sagi-Crab: saudação detectada — sem busca no Qdrant")

        system_prompt = """Você é o Sagi-Crab, membro da Turma AEB \
(Agência Espacial Brasileira). 🦀

🎯 MISSÃO:
Responder de forma geral e introdutória usando o contexto dos documentos.

🗣️ SAUDAÇÕES:
Se a mensagem for apenas uma saudação ("oi", "olá", "bom dia",
"boa tarde", "boa noite", "tudo bem" etc.):
- Responda com a saudação correspondente de forma animada
- Apresente-se brevemente como membro da Turma AEB
- Pergunte o que o usuário deseja saber
- NÃO cite documentos nem faça buscas
- NÃO delegue para especialistas neste caso

Exemplo:
Usuário: "boa noite"
Resposta: "Boa noite! 🦀 Sou o Sagi-Crab, membro da Turma AEB.
Fico feliz em ter você aqui! O que você gostaria de saber sobre
a Agência Espacial Brasileira hoje?"

🗣️ ESTILO GERAL:
- Tom animado, acolhedor e didático 🦀
- Respostas gerais e introdutórias — não entre em detalhes profundos
- Máximo 2 parágrafos curtos
- Use emojis com moderação

⚠️ REGRAS CRÍTICAS:
1. Use APENAS informações do contexto fornecido
2. NUNCA invente dados, números, artigos ou nomes
3. Se não houver contexto suficiente: diga que não encontrou a informação
   e sugira consultar o especialista ou aeb.gov.br
4. Cite a fonte: "Conforme pág. X de [nome do documento]..."
5. NÃO adicione mensagem de delegação ao final — isso é feito automaticamente
"""

        # prompt varia conforme saudação, contexto ou sem contexto
        if saudacao:
            prompt = f"Mensagem do usuário: {user_input}"

        elif context:
            prompt = f"""Contexto dos documentos AEB:
{context}

Pergunta: {user_input}

Responda em no máximo 1 parágrafo curto.
Cite sempre a fonte: "Conforme pág. X de [nome do documento]..."
NÃO adicione mensagem de delegação ao final — isso é feito automaticamente."""

        else:
            prompt = f"""Não encontrei informações específicas nos documentos.

Pergunta: {user_input}

Informe que não encontrou a informação nos documentos disponíveis \
e sugira consultar o especialista correto ou aeb.gov.br. \
NÃO invente informações."""

        messages[-1]["content"] = prompt

        input_messages = [
            {"role": "system", "content": system_prompt}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in messages[-5:]
        ]

        reply = get_response(self.client, self.model_name, input_messages)

        # ✅ delegação garantida via Python — sempre aparece, sem duplicar
        if not saudacao:
            domain = self.get_domain_from_context(context)
            reply += DELEGACAO[domain]

        return self.postprocess(reply)

    def postprocess(self, response: str) -> Dict:
        return {
            "role": "assistant",
            "content": response,
            "metadata": {
                "agent":  "sagicrab",
                "source": "agentic_rag",
            },
        }
