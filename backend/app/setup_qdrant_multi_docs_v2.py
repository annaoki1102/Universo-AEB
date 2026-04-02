"""
Setup Qdrant - Versão Multi-Documentos v2
Melhorias:
- Modelo multilíngue (pt-BR)
- Chunking por sentença (nltk)
- Metadados: authority, recency, agent
- Reranker após busca
- Hierarquia de fontes inteligente
"""

import os
import time
import re
from typing import List, Dict
from dotenv import load_dotenv

import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)
from tqdm import tqdm

load_dotenv()

# ─────────────────────────────────────────────────────────────
# DOCUMENTOS — adicione seus PDFs aqui
# authority : 0.0–1.0  (fonte oficial = 1.0, relatório = 0.6)
# recency   : 0.0–1.0  (mais recente = 1.0)
# agent     : quem deve usar este documento
# ─────────────────────────────────────────────────────────────
DOCUMENTS = [
    {
        "path": "/mnt/c/Users/eliaquim.ramos/Documents/eventos-marcos-pontes/backend/relatorio-de-gestao-aeb-2024.pdf",
        "name": "Relatório de Gestão AEB 2024",
        "doc_id": "relatorio-gestao-2024",
        "doc_type": "relatorio_gestao",
        "authority": 0.6,   # secundário — cita outras fontes
        "recency": 1.0,     # mais atualizado
        "agent": "cosminho",
    },
    # Descomente quando tiver o PDF da PNAE:
     {
         "path": "/mnt/c/Users/eliaquim.ramos/Documents/eventos-marcos-pontes/backend/PNAE 2022-2031 v1.05.pdf",
        "name": "PNAE 2022-2031",
         "doc_id": "pnae-2022",
        "doc_type": "legislacao",
         "authority": 1.0,   # fonte primária oficial
        "recency": 0.2,
         "agent": "luana",
     },

     {
    "path": "/mnt/c/Users/eliaquim.ramos/Documents/eventos-marcos-pontes/backend/Missao.pdf",
    "name": "Missão Centenário — 10 Anos",
    "doc_id": "missao-centenario",
    "doc_type": "missao_espacial",
    "authority": 0.9,
    "recency": 0.5,
    "agent": "sagicrab",   # ← só o Sagi-Crab responde
},

    # {
    #     "path": "/caminho/lei-9994-2000.pdf",
    #     "name": "Lei do Espaço nº 9.994/2000",
    #     "doc_id": "lei-espaco-9994",
    #     "doc_type": "legislacao",
    #     "authority": 1.0,
    #     "recency": 0.4,
    #     "agent": "luana",
    # },
]

COLLECTION_NAME = "aeb_documentos"

QDRANT_HOST    = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT    = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

# Chunking
SMALL_PAGE_THRESHOLD = 200   # palavras — página vai inteira
MAX_CHUNK_WORDS      = 400   # tamanho máximo do chunk
CHUNK_OVERLAP_SENTS  = 2     # sentenças de sobreposição entre chunks

# Modelos
EMBEDDING_MODEL = "intfloat/multilingual-e5-large"   # pt-BR nativo
RERANKER_MODEL  = "cross-encoder/ms-marco-MiniLM-L-6-v2"


# ─────────────────────────────────────────────────────────────
# EXTRAÇÃO
# ─────────────────────────────────────────────────────────────

def extract_text_from_pdf(doc_info: Dict) -> List[Dict]:
    """Extrai texto página a página com metadados do documento."""
    path = doc_info["path"]
    print(f"\n📄 Extraindo: {doc_info['name']}")

    if not os.path.exists(path):
        print(f"   ❌ Arquivo não encontrado: {path}")
        return []

    pages = []
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total = len(reader.pages)
            print(f"   Páginas: {total}")

            for i in tqdm(range(total), desc=f"  {doc_info['name'][:35]}"):
                text = reader.pages[i].extract_text() or ""
                if text.strip():
                    pages.append({
                        "page": i + 1,
                        "text": text,
                        **{k: doc_info[k] for k in
                           ("doc_id", "name", "doc_type",
                            "authority", "recency", "agent")},
                    })

        print(f"   ✅ {len(pages)} páginas extraídas")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

    return pages


# ─────────────────────────────────────────────────────────────
# LIMPEZA
# ─────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\x00", "")
    # remove cabeçalhos/rodapés comuns em PDFs governamentais
    text = re.sub(r"Página \d+ de \d+", "", text, flags=re.IGNORECASE)
    return text.strip()


# ─────────────────────────────────────────────────────────────
# CHUNKING POR SENTENÇA
# ─────────────────────────────────────────────────────────────

def chunk_by_sentences(text: str, max_words: int = MAX_CHUNK_WORDS,
                        overlap: int = CHUNK_OVERLAP_SENTS) -> List[str]:
    """
    Divide o texto em chunks respeitando fronteiras de sentença.
    Garante que nenhuma frase seja cortada no meio.
    """
    sentences = sent_tokenize(text, language="portuguese")
    chunks, current, current_words = [], [], 0

    for sent in sentences:
        words = len(sent.split())
        if current_words + words > max_words and current:
            chunks.append(" ".join(current))
            # overlap: mantém as últimas N sentenças no próximo chunk
            current = current[-overlap:] if overlap else []
            current_words = sum(len(s.split()) for s in current)

        current.append(sent)
        current_words += words

    if current:
        chunks.append(" ".join(current))

    return chunks


def create_chunks(all_pages: List[Dict]) -> List[Dict]:
    """Cria chunks inteligentes para todas as páginas."""
    print(f"\n✂️  Chunking por sentença (pt-BR)...")
    print(f"   Modelo NLTK: portuguese")
    print(f"   Max palavras/chunk: {MAX_CHUNK_WORDS}")
    print(f"   Overlap: {CHUNK_OVERLAP_SENTS} sentenças")

    chunks = []
    chunk_id = 0
    doc_stats: Dict[str, Dict] = {}

    for page in all_pages:
        text = clean_text(page["text"])
        words = text.split()
        doc_id = page["doc_id"]

        if doc_id not in doc_stats:
            doc_stats[doc_id] = {"name": page["name"], "chunks": 0}

        # Página pequena — vai inteira
        if len(words) <= SMALL_PAGE_THRESHOLD:
            chunks.append({
                "id": chunk_id,
                "text": text,
                "metadata": {
                    "page": page["page"],
                    "chunk_type": "full_page",
                    "chunk_size": len(words),
                    "doc_id": page["doc_id"],
                    "doc_name": page["name"],
                    "doc_type": page["doc_type"],
                    "authority": page["authority"],
                    "recency": page["recency"],
                    "agent": page["agent"],
                },
            })
            chunk_id += 1
            doc_stats[doc_id]["chunks"] += 1

        # Página grande — chunking por sentença
        else:
            for idx, chunk_text in enumerate(chunk_by_sentences(text)):
                if len(chunk_text.split()) < 30:
                    continue
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        "page": page["page"],
                        "chunk_type": "sentence_chunk",
                        "chunk_index": idx,
                        "chunk_size": len(chunk_text.split()),
                        "doc_id": page["doc_id"],
                        "doc_name": page["name"],
                        "doc_type": page["doc_type"],
                        "authority": page["authority"],
                        "recency": page["recency"],
                        "agent": page["agent"],
                    },
                })
                chunk_id += 1
                doc_stats[doc_id]["chunks"] += 1

    print(f"   ✅ {len(chunks)} chunks criados")
    print(f"\n   📊 Por documento:")
    for stats in doc_stats.values():
        print(f"      • {stats['name']}: {stats['chunks']} chunks")

    return chunks


# ─────────────────────────────────────────────────────────────
# QDRANT
# ─────────────────────────────────────────────────────────────

def init_qdrant() -> QdrantClient:
    print(f"\n🔌 Conectando ao Qdrant em {QDRANT_HOST}:{QDRANT_PORT}...")
    if QDRANT_API_KEY:
        client = QdrantClient(
            url=f"https://{QDRANT_HOST}",
            api_key=QDRANT_API_KEY,
            timeout=60,
        )
    else:
        client = QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            timeout=60,           # evita ReadTimeout em coleções grandes,  # remove aviso de versão incompatível
        )
    print("   ✅ Conectado")
    return client


def create_collection(client: QdrantClient, model: SentenceTransformer):
    print(f"\n📦 Coleção: {COLLECTION_NAME}")
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in existing:
        print("   ⚠️  Já existe — deletando para recriar...")
        client.delete_collection(COLLECTION_NAME)
        # aguarda o Qdrant finalizar a deleção antes de recriar
        time.sleep(2)
        print("   ✅ Deletada")

    dim = len(model.encode("teste"))
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
    )
    print(f"   ✅ Criada (dimensão: {dim})")


def upload_chunks(client: QdrantClient, chunks: List[Dict],
                  model: SentenceTransformer, batch_size: int = 64):
    print(f"\n⬆️  Enviando {len(chunks)} chunks (batch={batch_size})...")

    # prefixo necessário para o E5
    texts = [f"passage: {c['text']}" for c in chunks]
    points = []

    for i, (chunk, text) in enumerate(
            tqdm(zip(chunks, texts), total=len(chunks), desc="Embeddings")):

        emb = model.encode(text, normalize_embeddings=True)

        points.append(PointStruct(
            id=chunk["id"],
            vector=emb.tolist(),
            payload={
                "text":       chunk["text"],
                "page":       chunk["metadata"]["page"],
                "chunk_type": chunk["metadata"]["chunk_type"],
                "chunk_size": chunk["metadata"]["chunk_size"],
                "doc_id":     chunk["metadata"]["doc_id"],
                "doc_name":   chunk["metadata"]["doc_name"],
                "doc_type":   chunk["metadata"]["doc_type"],
                "authority":  chunk["metadata"]["authority"],
                "recency":    chunk["metadata"]["recency"],
                "agent":      chunk["metadata"]["agent"],
            },
        ))

        if len(points) >= batch_size:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            points = []

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"   ✅ Upload concluído")


# ─────────────────────────────────────────────────────────────
# BUSCA COM RERANKER E SCORE COMBINADO
# ─────────────────────────────────────────────────────────────

def compute_score(semantic: float, authority: float, recency: float,
                  query_type: str = "geral") -> float:
    """
    Combina score semântico com autoridade e recência.
    query_type:
      'definicao'   → prioriza fonte oficial  (authority)
      'dados_atuais'→ prioriza dado mais novo  (recency)
      'geral'       → equilibrado
    """
    weights = {
        "definicao":    (0.7, 0.3),   # (w_authority, w_recency)
        "dados_atuais": (0.3, 0.7),
        "geral":        (0.5, 0.5),
    }
    w_auth, w_rec = weights.get(query_type, (0.5, 0.5))
    source_score = w_auth * authority + w_rec * recency
    return semantic * source_score


def search(client: QdrantClient, model: SentenceTransformer,
           reranker: CrossEncoder, query: str,
           query_type: str = "geral",
           agent_filter: str = None,
           top_k: int = 10, top_rerank: int = 4) -> List[Dict]:
    """
    Busca vetorial → reranker → score combinado.
    agent_filter: se informado, busca apenas nos docs daquele agente.
    """
    # prefixo E5 para queries
    query_emb = model.encode(
        f"query: {query}", normalize_embeddings=True)

    # filtro opcional por agente
    qdrant_filter = None
    if agent_filter:
        qdrant_filter = Filter(must=[
            FieldCondition(key="agent",
                           match=MatchValue(value=agent_filter))
        ])

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_emb.tolist(),
        limit=top_k,
        query_filter=qdrant_filter,
    ).points

    if not results:
        return []

    # reranker
    pairs = [(query, r.payload["text"]) for r in results]
    rerank_scores = reranker.predict(pairs)

    # score combinado
    scored = []
    for r, rr_score in zip(results, rerank_scores):
        final = compute_score(
            semantic=float(rr_score),
            authority=r.payload.get("authority", 0.5),
            recency=r.payload.get("recency", 0.5),
            query_type=query_type,
        )
        scored.append({"result": r, "score": final,
                        "rerank": rr_score, "semantic": r.score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_rerank]


# ─────────────────────────────────────────────────────────────
# TESTE
# ─────────────────────────────────────────────────────────────

def run_tests(client: QdrantClient, model: SentenceTransformer,
              reranker: CrossEncoder):
    print(f"\n🔍 Testes de busca com reranker + score combinado\n")

    test_cases = [
        {
            "query": "Quais são os objetivos da PNAE?",
            "query_type": "definicao",
            "agent": None,
        },
        {
            "query": "Quantos servidores a AEB tinha em 2024?",
            "query_type": "dados_atuais",
            "agent": "cosminho",
        },
         {
        "query": "Quem é o presidente da AEB?",
        "query_type": "dados_atuais",
        "agent": None,
    },
        {
            "query": "A AEB cumpriu as metas do programa espacial?",
            "query_type": "geral",
            "agent": None,
        },
    ]

    for case in test_cases:
        print(f"  Query      : {case['query']}")
        print(f"  Tipo       : {case['query_type']}")
        print(f"  Agente     : {case['agent'] or 'todos'}")

        hits = search(
            client, model, reranker,
            query=case["query"],
            query_type=case["query_type"],
            agent_filter=case["agent"],
        )

        if hits:
            print(f"  Resultados :")
            for i, h in enumerate(hits, 1):
                p = h["result"].payload
                print(f"    {i}. [{p['doc_name'][:28]}]"
                      f" pág {p['page']}"
                      f" | auth={p['authority']}"
                      f" | rec={p['recency']}"
                      f" | score={h['score']:.3f}")
                print(f"       {p['text'][:90]}...")
        else:
            print("  ⚠️  Nenhum resultado")
        print()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("🚀  SETUP QDRANT — AEB MULTI-DOCUMENTOS v2")
    print("=" * 65)

    # NLTK
    print("\n📥 Verificando NLTK punkt...")
    try:
        nltk.data.find("tokenizers/punkt")
        print("   ✅ Já instalado")
    except LookupError:
        nltk.download("punkt")
        nltk.download("punkt_tab")

    # Documentos
    print(f"\n📚 Documentos configurados:")
    for d in DOCUMENTS:
        print(f"   • {d['name']}")
        print(f"     doc_type={d['doc_type']}"
              f"  authority={d['authority']}"
              f"  recency={d['recency']}"
              f"  agent={d['agent']}")

    # Modelos
    print(f"\n🤖 Carregando modelos...")
    print(f"   Embedding : {EMBEDDING_MODEL}")
    embed_model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"   Reranker  : {RERANKER_MODEL}")
    reranker = CrossEncoder(RERANKER_MODEL)
    print("   ✅ Modelos prontos")

    # Extração
    all_pages = []
    for doc in DOCUMENTS:
        all_pages.extend(extract_text_from_pdf(doc))

    if not all_pages:
        print("\n❌ Nenhuma página extraída. Verifique os caminhos dos PDFs.")
        return

    print(f"\n📊 Total de páginas extraídas: {len(all_pages)}")

    # Chunking
    chunks = create_chunks(all_pages)

    # Qdrant
    client = init_qdrant()
    create_collection(client, embed_model)
    upload_chunks(client, chunks, embed_model)

    # Testes
    run_tests(client, embed_model, reranker)

    # Resumo
    print("=" * 65)
    print("✅  SETUP CONCLUÍDO")
    print("=" * 65)
    print(f"   Documentos  : {len(DOCUMENTS)}")
    print(f"   Páginas     : {len(all_pages)}")
    print(f"   Chunks      : {len(chunks)}")
    print(f"   Coleção     : {COLLECTION_NAME}")
    print(f"   Embedding   : {EMBEDDING_MODEL}")
    print(f"   Reranker    : {RERANKER_MODEL}")
    print("=" * 65)


if __name__ == "__main__":
    main()
