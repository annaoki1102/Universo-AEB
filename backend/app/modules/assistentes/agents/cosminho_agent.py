"""
CosminhoAgent — Agentic RAG
Especialista técnico da Turma AEB:
- Satélites, lançamentos, missões, CLA
- Relatório de Gestão AEB 2024
- Dados técnicos e resultados do programa espacial
"""

#from anthropic import Anthropic
from .utils import get_response
from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from copy import deepcopy
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Optional
import json

load_dotenv()


# ─────────────────────────────────────────────────────────────
# AGENTIC RAG — sem alterações na lógica, só filtro por agente
# ─────────────────────────────────────────────────────────────

class AgenticRAG:
    """
    Sistema RAG inteligente — mesma lógica do general_agent_agentic.py
    Adaptação: filtro por agent="cosminho" no Qdrant
    """

    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedder: SentenceTransformer
    ):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.embedder = embedder

        print("   📊 Carregando reranker...")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        print("   ✅ Reranker carregado")

    def analyze_query(self, query: str) -> Dict:
        """Mesma lógica original — detecta tipo e complexidade."""
        query_lower = query.lower()

        analysis = {
            "type": "exploratory",
            "is_about_people": False,
            "is_about_projects": False,
            "complexity": "medium",
            "needs_filter": False,
            "filter_section": None,
        }

        people_keywords = [
            "quem é", "quem são", "presidente", "diretor",
            "diretora", "procurador", "auditor", "coordenador",
            "chefe", "assessor"
        ]
        if any(kw in query_lower for kw in people_keywords):
            analysis.update({
                "is_about_people": True,
                "type": "factual",
                "needs_filter": True,
                "filter_section": "dirigentes",
                "complexity": "low"
            })

        project_keywords = [
            "projeto", "satélite", "missão", "programa",
            "itasat", "aldebaran", "cbers", "amazonia",
            "alcântara", "vls", "vlm", "cla"
        ]
        if any(kw in query_lower for kw in project_keywords):
            analysis.update({
                "is_about_projects": True,
                "type": "exploratory",
                "complexity": "medium"
            })

        compare_keywords = ["compare", "diferença", "comparação", "versus", "vs"]
        if any(kw in query_lower for kw in compare_keywords):
            analysis.update({"type": "comparative", "complexity": "high"})

        if len(query.split()) > 15 or query.count("?") > 1:
            analysis["complexity"] = "high"

        return analysis

    def decide_strategy(self, query: str, analysis: Dict) -> Dict:
        """Mesma lógica original."""
        strategy = {
            "top_k": 15,
            "use_reranking": True,
            "page_range": None,
            "expand_search": False
        }

        if analysis["is_about_people"]:
            strategy.update({
                "top_k": 10,
                "page_range": [1, 30],
                "expand_search": False
            })
            print("   🎯 Estratégia: DIRIGENTES (páginas 1-30, top_k=10)")

        elif analysis["type"] == "comparative":
            strategy.update({"top_k": 30, "expand_search": True})
            print("   🎯 Estratégia: COMPARATIVA (top_k=30)")

        elif analysis["complexity"] == "high":
            strategy["top_k"] = 25
            print("   🎯 Estratégia: COMPLEXA (top_k=25)")

        elif analysis["complexity"] == "low":
            strategy["top_k"] = 10
            print("   🎯 Estratégia: FACTUAL (top_k=10)")

        else:
            print("   🎯 Estratégia: PADRÃO (top_k=15)")

        return strategy

    def execute_search(self, query: str, strategy: Dict) -> List:
        """
        Busca no Qdrant sem filtro por agent, para testar a recuperação
        de documentos e validar se o problema estava no filtro.
        """
        query_emb = self.embedder.encode(
            f"query: {query}",
            normalize_embeddings=True
        ).tolist()

        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_emb,
            limit=strategy["top_k"],
            with_payload=True,
        ).points

        return results

    def rerank_results(self, query: str, results: List, top_k: int) -> List:
        """Mesma lógica original."""
        if not results or len(results) <= 1:
            return results

        pairs = [[query, r.payload["text"]] for r in results]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [r for r, _ in ranked]

    def evaluate_results(self, results: List, analysis: Dict) -> Dict:
        """Mesma lógica original."""
        if not results:
            return {
                "sufficient": False,
                "confidence": 0.0,
                "needs_expansion": True
            }

        top_scores = [r.score for r in results[:3] if hasattr(r, "score")]
        avg_score = sum(top_scores) / len(top_scores) if top_scores else 0.5
        threshold = 0.25 if analysis["type"] == "factual" else 0.18

        return {
            "sufficient": avg_score >= threshold,
            "confidence": avg_score,
            "needs_expansion": avg_score < 0.15
        }

    def format_context(self, results: List) -> Optional[str]:
        """
        ✅ ADAPTAÇÃO: mostra doc_name além da página
        """
        if not results:
            return None

        parts = []
        for i, hit in enumerate(results, 1):
            page = hit.payload.get("page", "?")
            doc_name = hit.payload.get("doc_name", "AEB 2024")
            text = hit.payload.get("text", "")
            score = getattr(hit, "score", 0.0)

            parts.append(
                f"[Trecho {i} — {doc_name} | Pág. {page} | "
                f"Relevância: {score:.3f}]\n{text}"
            )

        return "\n\n" + "=" * 60 + "\n\n".join(parts)

    def query(self, user_query: str) -> Optional[str]:
        """Fluxo principal — idêntico ao original."""
        print("🚀 Cosminho Agentic RAG: Processando...")

        analysis = self.analyze_query(user_query)
        print(f"   📊 {analysis['type']} | complexidade: {analysis['complexity']}")

        strategy = self.decide_strategy(user_query, analysis)

        print("   🔍 Buscando chunks...")
        results = self.execute_search(user_query, strategy)
        print(f"   └─ {len(results)} chunks encontrados")

        if not results:
            print("   ⚠️  Nenhum resultado")
            return None

        if strategy["use_reranking"]:
            print("   🔄 Reranking...")
            results = self.rerank_results(
                user_query,
                results,
                top_k=min(10, len(results))
            )
            print(f"   └─ Top {len(results)} reordenados")

        evaluation = self.evaluate_results(results, analysis)
        print(f"   ✅ Confiança: {evaluation['confidence']:.3f}")

        if evaluation["needs_expansion"] and strategy.get("expand_search"):
            print("   🔄 Expandindo busca...")
            strategy["top_k"] = min(strategy["top_k"] * 2, 40)
            strategy["page_range"] = None
            results = self.execute_search(user_query, strategy)

            if strategy["use_reranking"]:
                results = self.rerank_results(user_query, results, top_k=15)

            print(f"   └─ {len(results)} chunks após expansão")

        return self.format_context(results)


# ─────────────────────────────────────────────────────────────
# COSMINHO AGENT
# ─────────────────────────────────────────────────────────────

class CosminhoAgent:
    """
    Cosminho — especialista técnico da Turma AEB.
    Satélites, lançamentos, CLA, missões, resultados do programa espacial.
    """

    def __init__(self) -> None:
        #self.client = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))
        #self.model_name = getenv("MODEL_NAME", "claude-sonnet-4-20250514")

        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        #self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"), base_url="https://chat.maritaca.ai/api")
        self.model_name = getenv("MODEL_NAME", "gpt-4o-mini")

        print("   📊 Carregando embeddings (multilingual-e5-large)...")
        self.embedder = SentenceTransformer("intfloat/multilingual-e5-large")
        print("   ✅ Embeddings carregados")

        self.collection_name = getenv("QDRANT_COLLECTION", "aeb_documentos")
        qdrant_host = getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(getenv("QDRANT_PORT", "6333"))
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
                c.name for c in self.qdrant_client.get_collections().collections
            ]

            if self.collection_name in collections:
                self.use_qdrant = True
                print(f"   ✅ Qdrant conectado — coleção: {self.collection_name}")

                self.agentic_rag = AgenticRAG(
                    qdrant_client=self.qdrant_client,
                    collection_name=self.collection_name,
                    embedder=self.embedder,
                )
                print("   ✅ Agentic RAG ativo")
            else:
                self.use_qdrant = False
                print(f"   ⚠️  Coleção '{self.collection_name}' não encontrada")

        except Exception as e:
            self.use_qdrant = False
            print(f"   ⚠️  Erro Qdrant: {e}")

        print("✅ CosminhoAgent: ativo")

    def respond(self, messages: List[Dict], query_type: str = "geral") -> Dict:
        """
        query_type vem do ClassifierAgent:
          'definicao'    → prioriza fonte oficial
          'dados_atuais' → prioriza relatório 2024
          'geral'        → equilibrado
        """
        messages = deepcopy(messages)
        user_input = messages[-1]["content"]

        context = None
        if self.use_qdrant:
            context = self.agentic_rag.query(user_input)
            if context:
                print("   ✅ Contexto obtido pelo Agentic RAG")
            else:
                print("   ⚠️  Nenhum contexto relevante encontrado")

        system_prompt = """Você é o Cosminho, assistente educacional animado \
da Turma AEB (Agência Espacial Brasileira). 🚀

🎯 ESPECIALIDADE TÉCNICA:
- Satélites brasileiros: CBERS, Amazonia-1, SCD, ITASAT, Aldebaran
- Centro de Lançamento de Alcântara (CLA)
- Veículos Lançadores (VLS, VLM)
- Missões espaciais e parcerias internacionais
- Orçamento, resultados e gestão da AEB
- INPE, DCTA e órgãos vinculados

📊 DOCUMENTOS DISPONÍVEIS:
Você tem acesso ao Relatório de Gestão AEB 2024 via busca semântica.

⚠️ REGRAS IMPORTANTES:
1. Priorize sempre o contexto dos documentos quando fornecido
2. Cite a fonte: "Conforme o Relatório de Gestão 2024 (pág. X)..."
3. Para dados específicos (números, nomes, orçamento): use APENAS o contexto
4. Se não tiver a informação: admita e sugira consultar aeb.gov.br
5. NUNCA invente dados, nomes ou números

🗣️ SAUDAÇÕES:
Se a mensagem for apenas uma saudação ("oi", "olá", "bom dia",
"boa tarde", "boa noite" etc.):
- Responda com a saudação de forma animada
- Apresente-se: "Sou o Cosminho, especialista técnico da Turma AEB! 🚀"
- Pergunte o que o usuário deseja saber sobre satélites, lançamentos ou missões
- NÃO cite documentos neste caso

Exemplo:
Usuário: "oi"
Resposta: "Oi! 🚀 Sou o Cosminho, especialista técnico da Turma AEB!
Posso te contar tudo sobre satélites, lançamentos e missões espaciais
brasileiras. O que você quer explorar hoje?"

🗣️ ESTILO:
- Tom animado e didático, acessível para estudantes e público geral
- Use emojis ocasionalmente 🚀🛸🌍
- Respostas curtas e diretas, ideais para leitura em voz alta
- Cite sempre a página do documento quando usar o contexto

🔀 DELEGAÇÃO:
Ao final de cada resposta, verifique o tema:
- Se envolver legislação, PNAE, normas, RH ou licitação → adicione:
  '⚖️ A Luana é especialista nesse tema! Troque de personagem no menu lateral para mais detalhes.'
- Se for puramente técnico (satélites, lançamentos, CLA) → não adicione nada.
"""

        if context:
            prompt = f"""Contexto dos documentos AEB:
{context}

Pergunta: {user_input}

Use o contexto acima para responder. Cite sempre a página de origem."""
        else:
            prompt = f"""Não encontrei informações específicas nos documentos disponíveis.

Pergunta: {user_input}

Responda com conhecimento geral sobre a AEB. Para dados específicos \
e atualizados, sugira consultar o Relatório de Gestão 2024 em aeb.gov.br."""

        messages[-1]["content"] = prompt

        input_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages[-5:]
        ]

        input_messages_with_system = [
            {"role": "system", "content": system_prompt}
        ] + input_messages

        reply = get_response(
            self.client,
            self.model_name,
            input_messages_with_system
        )
        return self.postprocess(reply)

    def postprocess(self, response: str) -> Dict:
        return {
            "role": "assistant",
            "content": response,
            "metadata": {
                "agent": "cosminho",
                "source": "agentic_rag",
            },
        }