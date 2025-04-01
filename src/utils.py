# utils.py
def get_keywords(user_input):
    # Dicionário de sinônimos
    keywords = {
        "horas trabalhadas": ["horas", "trabalhadas", "trabalho"],
        "atividades atrasadas": ["atividades", "atrasadas", "tarefas", "overdue"],
        "equipe do projeto": ["equipe", "membros", "time"],
        "status do projeto": ["status", "situação", "condição"]
    }

    user_input_lower = user_input.lower()
    for keyword, syns in keywords.items():
        if keyword in user_input_lower or any(syn in user_input_lower for syn in syns):
            return keyword  # Retorna a palavra-chave correspondente
    return None  # Retorna None se não encontrar correspondência
