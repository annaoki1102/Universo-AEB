"""
LuanaAgent — Agentic RAG
Especialista jurídica e normativa da Turma AEB:
- PNAE (Política Nacional de Atividades Espaciais)
- Lei 8.112/1990 (Regime Jurídico dos Servidores Federais)
- Lei 14.133/2021 (Licitações e Contratos)
- Normas e regulamentos da AEB
- RH do setor público federal
"""

from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from .utils import get_response
from copy import deepcopy
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List, Dict, Optional

load_dotenv()


# ─────────────────────────────────────────────────────────────
# AGENTIC RAG — mesma lógica do CosminhoAgent
# Única diferença: filtro agent="luana" e keywords jurídicas
# ─────────────────────────────────────────────────────────────

class AgenticRAG:
    """
    Sistema RAG inteligente para documentos jurídicos e normativos da AEB.
    Mesma lógica do CosminhoAgent — filtro por agent="luana".
    """

    def __init__(self, qdrant_client: QdrantClient, collection_name: str,
                 embedder: SentenceTransformer):
        self.qdrant = qdrant_client
        self.collection_name = collection_name
        self.embedder = embedder

        print("   📊 Carregando reranker...")
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("   ✅ Reranker carregado")

    def analyze_query(self, query: str) -> Dict:
        """
        Análise adaptada para domínio jurídico/normativo da Luana.
        """
        query_lower = query.lower()

        analysis = {
            "type": "exploratory",
            "is_about_people": False,
            "is_about_law": False,
            "is_about_rh": False,
            "complexity": "medium",
            "needs_filter": False,
        }

        # Perguntas sobre artigos e leis específicas
        law_keywords = ["artigo", "art.", "lei", "decreto", "portaria",
                        "instrução normativa", "resolução", "parágrafo",
                        "inciso", "alínea", "pnae", "8.112", "14.133"]
        if any(kw in query_lower for kw in law_keywords):
            analysis.update({"is_about_law": True, "type": "factual",
                              "complexity": "low"})

        # Perguntas sobre RH e gestão de pessoas
        rh_keywords = ["servidor", "concurso", "cargo", "salário", "férias",
                       "licença", "aposentadoria", "progressão", "rh",
                       "recursos humanos", "vacância", "exoneração"]
        if any(kw in query_lower for kw in rh_keywords):
            analysis.update({"is_about_rh": True, "type": "exploratory",
                              "complexity": "medium"})

        # Perguntas sobre licitação
        licitacao_keywords = ["licitação", "pregão", "contrato", "tcu",
                              "dispensa", "inexigibilidade", "edital",
                              "fornecedor", "compra"]
        if any(kw in query_lower for kw in licitacao_keywords):
            analysis.update({"type": "factual", "complexity": "medium"})

        # Perguntas comparativas
        compare_keywords = ["diferença", "compare", "versus", "vs",
                            "comparação", "qual a distinção"]
        if any(kw in query_lower for kw in compare_keywords):
            analysis.update({"type": "comparative", "complexity": "high"})

        # Perguntas complexas
        if len(query.split()) > 15 or query.count("?") > 1:
            analysis["complexity"] = "high"

        return analysis

    def decide_strategy(self, query: str, analysis: Dict) -> Dict:
        """Estratégia adaptada para documentos jurídicos."""
        strategy = {"top_k": 15, "use_reranking": True,
                    "page_range": None, "expand_search": False}

        if analysis["is_about_law"]:
            # Leis precisam de trechos precisos
            strategy.update({"top_k": 10, "expand_search": False})
            print("   🎯 Estratégia: JURÍDICA (top_k=10, alta precisão)")

        elif analysis["type"] == "comparative":
            strategy.update({"top_k": 30, "expand_search": True})
            print("   🎯 Estratégia: COMPARATIVA (top_k=30)")

        elif analysis["complexity"] == "high":
            strategy["top_k"] = 25
            print("   🎯 Estratégia: COMPLEXA (top_k=25)")

        elif analysis["is_about_rh"]:
            strategy["top_k"] = 15
            print("   🎯 Estratégia: RH (top_k=15)")

        else:
            print("   🎯 Estratégia: PADRÃO (top_k=15)")

        return strategy

    def execute_search(self, query: str, strategy: Dict) -> List:
        """
        Busca com filtro agent="luana" + prefixo E5.
        """
        query_emb = self.embedder.encode(
            f"query: {query}", normalize_embeddings=True).tolist()

        # ✅ filtro por agente — busca só nos docs da Luana
        agent_filter = Filter(must=[
            FieldCondition(key="agent",
                           match=MatchValue(value="luana"))
        ])

        if strategy["page_range"]:
            agent_filter.must.append(
                FieldCondition(
                    key="page",
                    range=Range(
                        gte=strategy["page_range"][0],
                        lte=strategy["page_range"][1],
                    ),
                )
            )

        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_emb,
            query_filter=agent_filter,
            limit=strategy["top_k"],
            with_payload=True,
        ).points

        return results

    def rerank_results(self, query: str, results: List, top_k: int) -> List:
        if not results or len(results) <= 1:
            return results
        pairs = [[query, r.payload["text"]] for r in results]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(results, scores),
                        key=lambda x: x[1], reverse=True)[:top_k]
        return [r for r, _ in ranked]

    def evaluate_results(self, results: List, analysis: Dict) -> Dict:
        if not results:
            return {"sufficient": False, "confidence": 0.0,
                    "needs_expansion": True}
        top_scores = [r.score for r in results[:3] if hasattr(r, "score")]
        avg_score = sum(top_scores) / len(top_scores) if top_scores else 0.5
        # Leis precisam de alta confiança
        threshold = 0.30 if analysis["is_about_law"] else 0.18
        return {"sufficient": avg_score >= threshold,
                "confidence": avg_score,
                "needs_expansion": avg_score < 0.15}

    def format_context(self, results: List) -> Optional[str]:
        if not results:
            return None
        parts = []
        for i, hit in enumerate(results, 1):
            page     = hit.payload.get("page", "?")
            doc_name = hit.payload.get("doc_name", "Documento AEB")
            text     = hit.payload.get("text", "")
            score    = getattr(hit, "score", 0.0)
            parts.append(
                f"[Trecho {i} — {doc_name} | Pág. {page} | "
                f"Relevância: {score:.3f}]\n{text}"
            )
        return "\n\n" + "="*60 + "\n\n".join(parts)

    def query(self, user_query: str) -> Optional[str]:
        print("⚖️  Luana Agentic RAG: Processando...")

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
                user_query, results, top_k=min(10, len(results)))
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
# LUANA AGENT
# ─────────────────────────────────────────────────────────────

class LuanaAgent:
    """
    Luana — especialista jurídica e normativa da Turma AEB.
    PNAE, Lei 8.112, Lei 14.133, RH público federal, normas AEB.
    """

    def __init__(self) -> None:
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.model_name = getenv("MODEL_NAME", "gpt-4o-mini")

        # ✅ modelo multilíngue pt-BR
        print("   📊 Carregando embeddings (multilingual-e5-large)...")
        self.embedder = SentenceTransformer("intfloat/multilingual-e5-large")
        print("   ✅ Embeddings carregados")

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

        print("✅ LuanaAgent: ativo")

    # ─── RESPOND ─────────────────────────────────────────────

    def respond(self, messages: List[Dict],
                query_type: str = "geral") -> Dict:
        messages = deepcopy(messages)
        user_input = messages[-1]["content"]

        # Busca Agentic RAG
        context = None
        if self.use_qdrant:
            context = self.agentic_rag.query(user_input)
            if context:
                print("   ✅ Contexto obtido pelo Agentic RAG")
            else:
                print("   ⚠️  Nenhum contexto relevante encontrado")

        # System prompt da Luana
        system_prompt = """Você é a Luana, assistente educacional especializada \
em legislação e normas do setor espacial brasileiro da Turma AEB. ⚖️

🎯 ESPECIALIDADE JURÍDICA E NORMATIVA:
- PNAE (Política Nacional de Atividades Espaciais 2022-2031)
- Lei do Espaço (Lei nº 9.994/2000)
- Lei 8.112/1990 (Regime Jurídico dos Servidores Federais)
- Lei 14.133/2021 (Licitações e Contratos Administrativos)
- Normas e regulamentos internos da AEB
- RH do setor público federal
- Acordos internacionais de uso do espaço

📊 DOCUMENTOS DISPONÍVEIS:
Você tem acesso à PNAE 2022-2031 e outros documentos normativos via busca semântica.

⚠️ REGRAS CRÍTICAS:
1. Priorize sempre o contexto dos documentos quando fornecido
2. Cite a fonte e artigo: "Conforme o Art. X da Lei 8.112/1990..."
3. Para artigos e números específicos: use APENAS o contexto fornecido
4. NUNCA invente artigos, leis ou números
5. Se não tiver a informação: admita e sugira consultar o Diário Oficial \
ou aeb.gov.br
6. Não forneça aconselhamento jurídico definitivo — sugira consultar \
o RH oficial da AEB para casos específicos

🗣️ SAUDAÇÕES:
Se a mensagem for apenas uma saudação:
- Apresente-se: "Sou a Luana, especialista jurídica da Turma AEB! ⚖️"
- Pergunte sobre legislação, PNAE ou normas
- NÃO cite documentos neste caso

🗣️ ESTILO:
- Tom profissional, claro e acessível
- Cite sempre a fonte legal: "Conforme Art. X da Lei Y..."
- Respostas objetivas, ideais para leitura em voz alta
- Use emojis com moderação ⚖️📋"

🔀 DELEGAÇÃO:
Ao final de cada resposta, verifique o tema:
- Se envolver satélites, lançamentos, CLA, missões ou dados técnicos → adicione:
  '🚀 O Cosminho é especialista nesse tema! Troque de personagem no menu lateral para mais detalhes.'
- Se for puramente jurídico/normativo → não adicione nada. """

        # Prompt com ou sem contexto
        if context:
            prompt = f"""Contexto dos documentos normativos AEB:
{context}

Pergunta: {user_input}

Use o contexto acima. Cite sempre o documento e página de origem. \
NUNCA invente artigos ou números que não estejam no contexto."""
        else:
            prompt = f"""Não encontrei informações específicas nos documentos disponíveis.

Pergunta: {user_input}

Responda com conhecimento geral sobre legislação espacial e RH público \
federal. Para artigos e dados específicos, sugira consultar:
- Diário Oficial da União (gov.br/diario-oficial-da-uniao)
- Portal da AEB (aeb.gov.br)
- Portal da Legislação (legislacao.gov.br)"""

        messages[-1]["content"] = prompt

        input_messages = [
            {"role": "system", "content": system_prompt}
        ] + [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages[-5:]
        ]

        response = get_response(self.client, self.model_name, input_messages)
        
        
        return self.postprocess(response)

    def postprocess(self, response: str) -> Dict:
        return {
            "role": "assistant",
            "content": response,
            "metadata": {
                "agent": "luana",
                "source": "agentic_rag",
            },
        }
