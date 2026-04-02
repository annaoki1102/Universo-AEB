from typing import Protocol, Dict, List, Any, Optional

class AgentProtocol(Protocol):
    def respond(
        self,
        messages: List[Dict[str, Any]],
        query_type: str = "geral"        # ← adicionar
    ) -> Dict[str, Any]:
        ...
