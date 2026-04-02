import logging
from functools import lru_cache
from typing import Any

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.modules.assistentes.controller import AgentController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()
USER_CHAT_HISTORY: dict[str, list[dict[str, Any]]] = {}


@lru_cache(maxsize=1)
def get_agent_controller() -> AgentController:
    return AgentController()


@router.post("/respond")
async def respond(input: dict[Any, Any] = Body(...)):
    try:
        if not input:
            return JSONResponse({"error": "Empty payload"}, status_code=400)

        entry = input.get("entry", [{}])[0]
        change = entry.get("changes", [{}])[0]
        value = change.get("value", {})

        messages = value.get("messages", [])
        if not messages:
            return JSONResponse({"error": "No messages in payload"}, status_code=400)

        first_msg = messages[0]
        if first_msg.get("type") != "text" or not first_msg.get("text"):
            return JSONResponse({"error": "Only text messages are supported"}, status_code=400)

        user_message_body = first_msg["text"]["body"]
        contacts = value.get("contacts", [])
        user_id = contacts[0]["wa_id"] if contacts else "web_user"
        character = contacts[0].get("character", "sagicrab") if contacts else "sagicrab"

        logger.info("[%s] (%s): %s", user_id, character, user_message_body)

        if user_id not in USER_CHAT_HISTORY:
            USER_CHAT_HISTORY[user_id] = []

        chat_history = USER_CHAT_HISTORY[user_id]
        chat_history.append({"role": "user", "content": user_message_body})

        agent_response = get_agent_controller().respond(chat_history, character=character)
        chat_history.append(agent_response)

        reply_text = agent_response.get(
            "content", "Desculpe, nao consegui processar sua mensagem."
        )

        return JSONResponse(
            {
                "status": "success",
                "message": reply_text,
                "user_id": user_id,
                "agent": agent_response.get("metadata", {}).get("agent", "unknown"),
            }
        )

    except KeyError as exc:
        logger.error("Formato invalido: %s", exc)
        return JSONResponse({"error": f"Invalid payload: missing {exc}"}, status_code=400)
    except Exception as exc:
        logger.error("Erro: %s", exc, exc_info=True)
        return JSONResponse({"error": f"Processing failed: {exc}"}, status_code=500)


@router.get("/")
async def root():
    return JSONResponse(
        {
            "name": "Turma AEB API",
            "version": "3.0.0",
            "description": "Sistema multi-agente da Agencia Espacial Brasileira",
            "endpoints": {
                "POST /respond": "Enviar mensagens para os agentes",
                "GET /health": "Verificar saude do sistema",
                "GET /agents": "Listar agentes ativos",
                "GET /history/{user_id}": "Ver historico de um usuario",
                "DELETE /history/{user_id}": "Limpar historico de um usuario",
                "GET /stats": "Estatisticas do sistema",
            },
            "status": "online",
        }
    )


@router.get("/health")
async def health_check():
    return JSONResponse(
        {
            "status": "healthy",
            "agents_loaded": get_agent_controller.cache_info().currsize > 0,
            "active_users": len(USER_CHAT_HISTORY),
        }
    )


@router.get("/agents")
async def list_agents():
    return JSONResponse(
        {
            "agents": [
                {
                    "name": "GuardAgent",
                    "description": "Filtra mensagens inadequadas",
                    "status": "active",
                },
                {
                    "name": "ClassifierAgent",
                    "description": "Sagi-Crab roteia para Cosminho ou Luana",
                    "status": "active",
                },
                {
                    "name": "CosminhoAgent",
                    "description": "Especialista tecnico da AEB",
                    "status": "active",
                },
                {
                    "name": "LuanaAgent",
                    "description": "Especialista juridica e normativa da AEB",
                    "status": "active",
                },
            ],
            "total": 4,
        }
    )


@router.get("/history/{user_id}")
async def get_history(user_id: str):
    if user_id not in USER_CHAT_HISTORY:
        return JSONResponse({"error": "User not found"}, status_code=404)
    return JSONResponse(
        {
            "user_id": user_id,
            "messages": USER_CHAT_HISTORY[user_id],
            "total_messages": len(USER_CHAT_HISTORY[user_id]),
        }
    )


@router.delete("/history/{user_id}")
async def clear_history(user_id: str):
    if user_id not in USER_CHAT_HISTORY:
        return JSONResponse({"error": "User not found"}, status_code=404)
    count = len(USER_CHAT_HISTORY[user_id])
    USER_CHAT_HISTORY[user_id] = []
    return JSONResponse(
        {
            "status": "success",
            "user_id": user_id,
            "messages_cleared": count,
        }
    )


@router.get("/stats")
async def get_stats():
    total_users = len(USER_CHAT_HISTORY)
    total_messages = sum(len(history) for history in USER_CHAT_HISTORY.values())
    return JSONResponse(
        {
            "total_users": total_users,
            "total_messages": total_messages,
            "avg_per_user": round(total_messages / total_users, 2) if total_users else 0,
        }
    )
