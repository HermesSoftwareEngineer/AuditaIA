"""
Serviço para análise e cálculos de dados financeiros
"""
from typing import Dict, List, Any

def analyze_movements(current_movements: Dict, previous_movements: Dict) -> Dict:
    """
    Analisa comparações de movimentações financeiras.
    Calcula métricas financeiras e fornece insights sobre as diferenças
    entre os movimentos do mês atual e do mês anterior.
    
    Args:
        current_movements: Dados de movimentações do período atual
        previous_movements: Dados de movimentações do período anterior
        
    Returns:
        dict: Resultados da análise incluindo métricas e insights
    """
    current_items = current_movements.get('lista', [])
    previous_items = previous_movements.get('lista', [])
    
    # Calcula totais diretamente sem listas intermediárias para evitar problemas de acumulação
    total_current = 0
    for item in current_items:
        item_total = sum(detail.get('valor', 0) for detail in item.get('detalhes_resumo', []))
        total_current += item_total
    
    # Para o mês anterior, seja extremamente cuidadoso com duplicatas
    # Use um conjunto para rastrear clientes que já contamos
    counted_clients = set()
    total_previous = 0
    
    for item in previous_items:
        # client = item.get('cliente', '')
        # # Pula se já contamos este cliente
        # if client in counted_clients:
        #     continue
            
        # counted_clients.add(client)
        item_total = sum(detail.get('valor', 0) for detail in item.get('detalhes_resumo', []))
        total_previous += item_total

    # Calcula a variação absoluta (mudança no valor)
    variacao_absoluta = total_current - total_previous
    
    # Calcula a variação percentual - trata o caso onde ambos os valores são negativos
    variacao_percentual = 0
    if total_previous != 0:
        # Se ambos são negativos, precisamos considerar a mudança de magnitude
        if total_current < 0 and total_previous < 0:
            # Calcula a mudança na magnitude (valores absolutos)
            magnitude_atual = abs(total_current)
            magnitude_anterior = abs(total_previous)
            
            if magnitude_atual < magnitude_anterior:
                # Magnitude diminuiu (ficando mais próximo de zero) - isso é uma redução
                variacao_percentual = -((magnitude_anterior - magnitude_atual) / magnitude_anterior * 100)
            else:
                # Magnitude aumentou (ficando mais longe de zero) - isso é um aumento
                variacao_percentual = ((magnitude_atual - magnitude_anterior) / magnitude_anterior * 100)
        else:
            # Cálculo percentual normal para outros casos
            variacao_percentual = (variacao_absoluta / abs(total_previous)) * 100
    
    # Adiciona descrições à variação - certifique-se de que corresponde ao sinal de variacao_percentual
    variacao_descricao = "sem alteração"
    if variacao_percentual > 0:
        variacao_descricao = f"aumento de {abs(round(variacao_percentual, 2))}%"
    elif variacao_percentual < 0:
        variacao_descricao = f"redução de {abs(round(variacao_percentual, 2))}%"
    
    analysis = {
        "resumo": "Análise comparativa de prestação de contas",
        "total_mes_atual": round(total_current, 2),
        "total_mes_anterior": round(total_previous, 2),
        "variacao_absoluta": round(variacao_absoluta, 2),
        "variacao_percentual": round(variacao_percentual, 2),
        "variacao_descricao": variacao_descricao,
        "insights": [
            "Comparação básica entre os meses realizada",
            f"Houve uma {variacao_descricao} no valor total dos movimentos",
            "Para análise detalhada, implemente integração com um modelo de IA mais avançado"
        ],
        "alertas": []
    }
    
    # Adicionar alertas se a variação for significativa
    if abs(variacao_percentual) > 20:
        analysis["alertas"].append(f"Variação significativa de {abs(round(variacao_percentual, 2))}% detectada entre os meses")
    
    return analysis
    
    
def calculate_client_metrics(client_data: Dict, previous_client_data: Dict = None) -> Dict:
    """
    Calcula métricas financeiras para um cliente específico
    
    Args:
        client_data: Dados do período atual para o cliente
        previous_client_data: Dados do período anterior para o cliente (opcional)
        
    Returns:
        dict: Métricas financeiras para o cliente
    """
    # Calcula o total atual
    current_total = sum(detail.get('valor', 0) for detail in client_data.get('detalhes_resumo', []))
    
    # Calcula o total anterior se os dados existirem
    prev_total = 0
    if previous_client_data:
        prev_total = sum(detail.get('valor', 0) for detail in previous_client_data.get('detalhes_resumo', []))
    
    # Calcula a diferença e a variação percentual
    difference = current_total - prev_total
    percentage_change = 0
    if prev_total != 0:
        percentage_change = (difference / prev_total) * 100
    
    return {
        'valor_total_atual': round(current_total, 2),
        'valor_total_anterior': round(prev_total, 2),
        'diferenca': round(difference, 2),
        'variacao_percentual': round(percentage_change, 2)
    }
