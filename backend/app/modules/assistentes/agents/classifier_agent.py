from ast import literal_eval
from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
from .utils import get_response
from copy import deepcopy

load_dotenv()


class ClassifierAgent:
    """
    Classifica a pergunta e roteia para Cosminho, Luana ou Sagi-Crab.
    Também detecta o query_type para ponderação do score no Agentic RAG.
    """

    def __init__(self) -> None:
        self.client     = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.model_name = getenv("MODEL_NAME")

    def respond(self, messages):
        messages = deepcopy(messages)

        system_prompt = """
Você é o classificador da Turma AEB (Agência Espacial Brasileira). 🦀

🎯 MISSÃO: Decidir qual agente deve responder E qual o tipo da pergunta.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENTE 1 — cosminho
Especialista técnico: satélites, lançamentos, missões, CLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCUMENTOS: Relatório de Gestão AEB 2024

TÓPICOS:
✓ Satélites: CBERS, Amazonia-1, SCD, ITASAT2, Aldebaran
✓ Centro de Lançamento de Alcântara (CLA)
✓ Veículos lançadores (VLS, VLM)
✓ Missões e programas espaciais
✓ Parcerias internacionais (China, EUA, ESA)
✓ Orçamento, resultados e gestão da AEB
✓ Estrutura organizacional (presidente, diretores)
✓ INPE, DCTA e órgãos vinculados

PALAVRAS-CHAVE:
satélite, missão, lançamento, foguete, Alcântara, CBERS,
Amazonia, VLS, VLM, CLA, orçamento, presidente, diretor,
resultado, programa espacial, cooperação internacional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENTE 2 — luana
Especialista jurídica: legislação, normas, RH, licitação
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCUMENTOS: PNAE 2022-2031, Lei 8.112, Lei 14.133

TÓPICOS:
✓ PNAE (Política Nacional de Atividades Espaciais)
✓ Lei do Espaço (Lei nº 9.994/2000)
✓ Lei 8.112/1990 (Regime Jurídico dos Servidores)
✓ Lei 14.133/2021 (Licitações e Contratos)
✓ RH: férias, licenças, benefícios, carreira, concurso
✓ Licitação: pregão, edital, TCU, contrato, dispensa
✓ Normas e regulamentos internos da AEB

PALAVRAS-CHAVE:
PNAE, lei, decreto, portaria, artigo, norma, regulamento,
licitação, pregão, contrato, TCU, edital, RH, servidor,
férias, licença, benefício, salário, concurso, CLT, 8.112

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENTE 3 — sagicrab
Coordenador geral: saudações, dúvidas gerais, navegação
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TÓPICOS:
✓ Saudações ("oi", "olá", "bom dia")
✓ Perguntas sobre a Turma AEB ("quem são vocês?")
✓ Dúvidas mistas que envolvem técnico E jurídico
✓ Pedidos de troca de personagem
✓ Perguntas vagas ou sem contexto claro
✓ Perguntas gerais sobre o espaço sem foco específico

PALAVRAS-CHAVE:
missão centenário, marcos pontes, astronauta brasileiro,
soyuz, ISS, estação espacial, baikonur, 2006, espaço

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUERY_TYPE — tipo da pergunta
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"definicao"    → pergunta sobre conceito, lei, política, o que é
"dados_atuais" → pergunta sobre números, resultados, status atual, 2024
"geral"        → outros

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXEMPLOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"O que é o ITASAT2?"
→ {"decision": "cosminho", "query_type": "definicao"}

"Qual foi o orçamento da AEB em 2024?"
→ {"decision": "cosminho", "query_type": "dados_atuais"}

"Onde fica o Centro de Lançamento de Alcântara?"
→ {"decision": "cosminho", "query_type": "definicao"}

"Quantos servidores a AEB tinha em 2024?"
→ {"decision": "cosminho", "query_type": "dados_atuais"}

"A AEB cumpriu as metas do programa espacial?"
→ {"decision": "cosminho", "query_type": "dados_atuais"}

"Quais são os objetivos da PNAE?"
→ {"decision": "luana", "query_type": "definicao"}

"O que é a Lei 8.112?"
→ {"decision": "luana", "query_type": "definicao"}

"Como funciona o pregão eletrônico?"
→ {"decision": "luana", "query_type": "definicao"}

"Como solicitar férias?"
→ {"decision": "luana", "query_type": "geral"}

"Como a AEB contrata fornecedores?"
→ {"decision": "luana", "query_type": "geral"}

"Como a AEB contrata funcionários?"
→ {"decision": "luana", "query_type": "geral"}

"Quais treinamentos a AEB oferece?"
→ {"decision": "luana", "query_type": "geral"}

"oi"
→ {"decision": "sagicrab", "query_type": "geral"}

"olá, tudo bem?"
→ {"decision": "sagicrab", "query_type": "geral"}

"quem são vocês?"
→ {"decision": "sagicrab", "query_type": "geral"}

"o que é a turma aeb?"
→ {"decision": "sagicrab", "query_type": "geral"}

"a luana poderia me responder?"
→ {"decision": "sagicrab", "query_type": "geral"}

"pode me passar para o cosminho?"
→ {"decision": "sagicrab", "query_type": "geral"}

"como o brasil se compara no cenário espacial mundial?"
→ {"decision": "sagicrab", "query_type": "geral"}

"me fale sobre o programa espacial brasileiro"
→ {"decision": "sagicrab", "query_type": "geral"}

"Quem foi Marcos Pontes?"
→ {"decision": "sagicrab", "query_type": "definicao"}

"O que foi a Missão Centenário?"
→ {"decision": "sagicrab", "query_type": "definicao"}

"Quando o Brasil foi ao espaço?"
→ {"decision": "sagicrab", "query_type": "definicao"}

"Quantos dias Marcos Pontes ficou na ISS?"
→ {"decision": "sagicrab", "query_type": "dados_atuais"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REGRAS DE DECISÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

0. Missão Centenário, Marcos Pontes, astronauta brasileiro,
   ISS, Soyuz, primeiro brasileiro no espaço → sagicrab   ← nova
1. Lei, norma, RH, licitação, servidor → luana
2. Satélite, lançamento, CLA, missão, orçamento, resultado → cosminho
3. PNAE → luana (é documento normativo)
4. Saudação, pedido de troca, dúvida vaga → sagicrab
5. Ambíguo entre técnico e jurídico → sagicrab
6. Sem contexto claro → sagicrab

⚙️ FORMATO DE RESPOSTA — JSON VÁLIDO EXATO:
{
  "chain of thought": "<raciocínio em 1 frase>",
  "decision": "cosminho" ou "luana" ou "sagicrab",
  "query_type": "definicao" ou "dados_atuais" ou "geral"
}

CRÍTICO:
• Escolha EXATAMENTE UM agente: "cosminho", "luana" ou "sagicrab"
• NÃO inclua markdown (```json)
• Retorne APENAS o objeto JSON
"""

        input_messages = [
            {"role": "system", "content": system_prompt}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in messages[-3:]
        ]

        response = get_response(self.client, self.model_name, input_messages)
        return self.postprocess(response)

    def postprocess(self, response):
        try:
            parsed = literal_eval(response)

            # ✅ sagicrab adicionado como agente válido
            valid_agents = ["cosminho", "luana", "sagicrab"]
            decision = parsed.get("decision", "sagicrab")

            if decision not in valid_agents:
                print(f"⚠️  Agente inválido: '{decision}' → fallback sagicrab")
                decision = "sagicrab"

            query_type = parsed.get("query_type", "geral")
            if query_type not in ("definicao", "dados_atuais", "geral"):
                query_type = "geral"

            print(f"🦀 Classifier → {decision} | {query_type}")

            return {
                "role": "assistant",
                "content": "",
                "metadata": {
                    "agent":      "classifier_agent",
                    "decision":   decision,
                    "query_type": query_type,
                    "reasoning":  parsed.get("chain of thought", ""),
                },
            }

        except Exception as e:
            print(f"❌ Erro no ClassifierAgent: {e}")
            print(f"   Resposta recebida: {response}")
            return {
                "role": "assistant",
                "content": "",
                "metadata": {
                    "agent":      "classifier_agent",
                    "decision":   "sagicrab",  # ✅ fallback para sagicrab
                    "query_type": "geral",
                    "error":      str(e),
                },
            }
