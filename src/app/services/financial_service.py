"""
Service for financial data analysis and calculations
"""
from typing import Dict, List, Any

def analyze_movements(current_movements: Dict, previous_movements: Dict) -> Dict:
    """
    Analyze financial movement comparisons.
    Calculates financial metrics and provides insights on the differences 
    between current and previous month's movements.
    
    Args:
        current_movements: The current period movements data
        previous_movements: The previous period movements data
        
    Returns:
        dict: Analysis results including metrics and insights
    """
    current_items = current_movements.get('lista', [])
    previous_items = previous_movements.get('lista', [])
    
    # Calculate totals directly without intermediate lists to avoid any accumulation issues
    total_current = 0
    for item in current_items:
        item_total = sum(detail.get('valor', 0) for detail in item.get('detalhes_resumo', []))
        total_current += item_total
    
    # For previous month, be extra careful about duplicates
    # Use a set to track clients we've already counted
    counted_clients = set()
    total_previous = 0
    
    for item in previous_items:
        client = item.get('cliente', '')
        # Skip if we've already counted this client
        if client in counted_clients:
            continue
            
        counted_clients.add(client)
        item_total = sum(detail.get('valor', 0) for detail in item.get('detalhes_resumo', []))
        total_previous += item_total

    # Calculate the absolute variation (change in value)
    variacao_absoluta = total_current - total_previous
    
    # Calculate percentage change - handle the case where both values are negative
    variacao_percentual = 0
    if total_previous != 0:
        # If both are negative, we need to consider the magnitude change
        if total_current < 0 and total_previous < 0:
            # Calculate change in magnitude (absolute values)
            magnitude_atual = abs(total_current)
            magnitude_anterior = abs(total_previous)
            
            if magnitude_atual < magnitude_anterior:
                # Magnitude decreased (getting closer to zero) - this is a reduction
                variacao_percentual = -((magnitude_anterior - magnitude_atual) / magnitude_anterior * 100)
            else:
                # Magnitude increased (getting further from zero) - this is an increase
                variacao_percentual = ((magnitude_atual - magnitude_anterior) / magnitude_anterior * 100)
        else:
            # Normal percentage calculation for other cases
            variacao_percentual = (variacao_absoluta / abs(total_previous)) * 100
    
    # Add descriptions to variation - make sure it matches the sign of variacao_percentual
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
    Calculate financial metrics for a specific client
    
    Args:
        client_data: Current period data for client
        previous_client_data: Previous period data for client (optional)
        
    Returns:
        dict: Financial metrics for the client
    """
    # Calculate current total
    current_total = sum(detail.get('valor', 0) for detail in client_data.get('detalhes_resumo', []))
    
    # Calculate previous total if data exists
    prev_total = 0
    if previous_client_data:
        prev_total = sum(detail.get('valor', 0) for detail in previous_client_data.get('detalhes_resumo', []))
    
    # Calculate difference and percentage change
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
