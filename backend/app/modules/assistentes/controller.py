from .agents import (
    AgentProtocol,
    ClassifierAgent,
    CosminhoAgent,
    GuardAgent,
    LuanaAgent,
    SagiCrabAgent,
)


class AgentController:
    """
    Controlador que orquestra o fluxo entre os agentes da Turma AEB.
    Fluxo: GuardAgent -> ClassifierAgent -> Cosminho, Luana ou SagiCrab.
    """

    def __init__(self):
        print("Initializing AgentController - Turma AEB...")

        self.guard_agent = GuardAgent()
        self.classifier_agent = ClassifierAgent()

        self.agent_dict: dict[str, AgentProtocol] = {
            "cosminho": CosminhoAgent(),
            "luana": LuanaAgent(),
            "sagicrab": SagiCrabAgent(),
        }

        print("AgentController initialized.")
        print("   - GuardAgent      : active")
        print("   - ClassifierAgent : active (Sagi-Crab)")
        print("   - CosminhoAgent   : active (satellites, launches, CLA)")
        print("   - LuanaAgent      : active (PNAE, Lei 8.112, bidding, HR)")
        print("   - SagiCrabAgent   : active (general, Missao Centenario)")

    def respond(self, messages: list, character: str = "sagicrab") -> dict:
        """
        Fluxo:
        1. GuardAgent filtra perguntas inadequadas.
        2. ClassifierAgent decide cosminho / luana / sagicrab + query_type.
        3. Se for saudacao ou pergunta vaga e o personagem ativo for Cosminho ou Luana,
           usa o personagem ativo em vez do Sagi-Crab.
        4. O agente escolhido gera a resposta com Agentic RAG.
        """

        guard_response = self.guard_agent.respond(messages)
        if guard_response["metadata"]["decision"] == "not allowed":
            print(f"Warning: GuardAgent blocked message: {messages[-1]['content'][:50]}...")
            return guard_response

        classifier_response = self.classifier_agent.respond(messages)
        if classifier_response["metadata"]["decision"] == "unknown":
            print("Warning: ClassifierAgent could not classify the message.")
            return classifier_response

        chosen_agent = classifier_response["metadata"]["decision"]
        query_type = classifier_response["metadata"].get("query_type", "geral")

        if chosen_agent == "sagicrab" and character in ("cosminho", "luana"):
            print(f"Routing greeting/general request to active character: {character}")
            chosen_agent = character

        print(f"Agent: {chosen_agent} | Type: {query_type} | Character: {character}")

        agent = self.agent_dict.get(chosen_agent)
        if agent is None:
            print(f"Warning: agent '{chosen_agent}' not found - falling back to sagicrab")
            agent = self.agent_dict["sagicrab"]

        return agent.respond(messages, query_type=query_type)
