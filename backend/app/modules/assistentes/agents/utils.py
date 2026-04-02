def get_response(client, model_name, messages, max_tokens=2000):
    """
    Função auxiliar para obter resposta do modelo LLM
    """
    response = client.chat.completions.create(
        messages=messages,
        model=model_name,
        max_completion_tokens=max_tokens,
    ).choices[0].message.content
    return response
