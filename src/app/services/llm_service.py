"""
Service for LLM (Language Learning Model) analysis
Contains both simulated and real analysis implementations
"""
from typing import Dict, Optional, Any
from ai.llms import llm

# You might need to import your real LLM service here
# from external.llm_provider import analyze_with_llm

class LLMAnalysisService:
    """
    Service for generating insights from financial data using LLM models
    """
    
    @staticmethod
    def simulate_analysis(
        client_name: str, 
        current_data: Dict, 
        previous_data: Optional[Dict], 
        current_total: float, 
        prev_total: float, 
        percentage_change: float
    ) -> str:
        """
        Simulate an LLM analysis for a specific client's movements.
        This function returns simulated insights text.
        
        Args:
            client_name: Name of the client
            current_data: Current month's data for this client
            previous_data: Previous month's data for this client
            current_total: Pre-calculated total for current month
            prev_total: Pre-calculated total for previous month
            percentage_change: Pre-calculated percentage change
            
        Returns:
            str: Simulated LLM insights text
        """
        # Start with basic analysis of totals
        insights = [
            f"As movimentações financeiras para {client_name} totalizaram {current_total:.2f} no mês atual."
        ]
        
        # Add comparison with previous month if available
        if prev_total > 0:
            change = current_total - prev_total
            direction = "redução" if change < 0 else "aumento"
            insights.append(f"Em comparação com o mês anterior ({prev_total:.2f}), houve uma {direction} de {abs(change):.2f} ({abs(percentage_change):.2f}%).")
        
        # Analyze categories with significant changes
        for detail in current_data.get('detalhes_resumo', []):
            account = detail.get('conta')
            value = detail.get('valor', 0)
            
            # Find matching previous month category
            prev_value = 0
            if previous_data:
                for prev_detail in previous_data.get('detalhes_resumo', []):
                    if prev_detail.get('conta') == account:
                        prev_value = prev_detail.get('valor', 0)
                        break
            
            # Calculate percentage change for this category
            cat_percentage = 0
            if prev_value != 0:
                cat_change = value - prev_value
                cat_percentage = (cat_change / prev_value) * 100
                
                # Only add insights for significant changes
                if abs(cat_percentage) > 15:
                    direction = "aumento" if cat_percentage > 0 else "redução"
                    insights.append(f"Houve {direction} significativo de {abs(cat_percentage):.2f}% na categoria {account}.")
        
        # Add recommendations based on overall change
        if percentage_change < -10:
            insights.append(f"Recomendo analisar a queda de {abs(percentage_change):.2f}% nas movimentações em relação ao mês anterior.")
        elif percentage_change > 10:
            insights.append(f"O aumento de {percentage_change:.2f}% em relação ao mês anterior indica uma tendência positiva.")
        
        # Add alert for missing historical data
        if not previous_data:
            insights.append(f"Não há dados históricos disponíveis para {client_name} no mês anterior.")
        
        # Join all insights into a single text
        return "\n".join(insights)

    @staticmethod
    def perform_real_analysis(
        client_name: str, 
        current_data: Dict, 
        previous_data: Optional[Dict], 
        current_total: float, 
        prev_total: float, 
        percentage_change: float
    ) -> str:
        """
        Perform a real LLM analysis for a specific client's movements.
        
        Args:
            client_name: Name of the client
            current_data: Current month's data for this client
            previous_data: Previous month's data for this client
            current_total: Pre-calculated total for current month
            prev_total: Pre-calculated total for previous month
            percentage_change: Pre-calculated percentage change
            
        Returns:
            str: Real LLM insights text
        """
        # If there's no variation between months, return a simple message
        if percentage_change == 0 and current_total == prev_total:
            return f"Para o cliente {client_name} não houve variação nos valores entre o mês atual e o mês anterior. O valor total se manteve em R$ {current_total:.2f}."
            
        # Prepare the prompt for LLM with relevant financial data
        prompt = f"""
        Analise os movimentos de um repasse de um proprietário de um imóvel alugado. A inquilina do imóvel é {client_name}:
        
        Mês atual:
        - Total: R$ {current_total:.2f}
        - Detalhes por categoria: {current_data.get('detalhes_resumo', [])}
        
        Mês anterior:
        - Total: R$ {prev_total:.2f}
        - Detalhes por categoria: {previous_data.get('detalhes_resumo', []) if previous_data else 'Dados não disponíveis'}
        
        Variação percentual: {percentage_change:.2f}%
        
        Seja curto, breve, direto e use poucas palavras pra responder:
        1. Qual o motivo da variação?
            - Se não houver variação, apenas confirme que não houve nenhuma mudança aparente.
            - Se houver variação, detalhe os movimentos (valor, conta e descrição)
        """
        
        # Here you would call your actual LLM service
        # This is a placeholder - replace with your actual LLM integration
        try:
            # Example of how you might call your LLM service
            # result = analyze_with_llm(prompt)
            # return result
            
            # For now, return a placeholder message
            result = llm.invoke(prompt)
            return result.content
        except Exception as e:
            # Fallback to simulated analysis in case of error
            print(f"Erro ao chamar LLM real: {str(e)}")
            return f"Erro na análise de IA. Utilizando análise simulada: " + LLMAnalysisService.simulate_analysis(
                client_name, current_data, previous_data, current_total, prev_total, percentage_change
            )
            
    @staticmethod
    def get_client_insights(
        client_name: str,
        client_data: Dict,
        previous_client_data: Optional[Dict],
        metrics: Dict,
        use_real_llm: bool = False
    ) -> str:
        """
        Get insights for a client based on financial data
        
        Args:
            client_name: Name of the client
            client_data: Current period data for client
            previous_client_data: Previous period data for client
            metrics: Pre-calculated financial metrics
            use_real_llm: Whether to use real LLM analysis
            
        Returns:
            str: Insights for the client
        """
        current_total = metrics['valor_total_atual']
        prev_total = metrics['valor_total_anterior']
        percentage_change = metrics['variacao_percentual']
        
        # Check if there's any variation between months
        has_variation = (percentage_change != 0) or (current_total != prev_total)
        
        # Use real LLM if requested
        if use_real_llm:
            return LLMAnalysisService.perform_real_analysis(
                client_name,
                client_data,
                previous_client_data,
                current_total,
                prev_total,
                percentage_change
            )
        else:
            # For the simulated analysis, if there's no variation, provide a simple message
            if not has_variation:
                return f"Para o cliente {client_name} não houve variação nos valores entre o mês atual e o mês anterior. O valor total se manteve em R$ {current_total:.2f}."
            else:
                return LLMAnalysisService.simulate_analysis(
                    client_name,
                    client_data,
                    previous_client_data,
                    current_total,
                    prev_total,
                    percentage_change
                )
