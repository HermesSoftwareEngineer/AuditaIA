from flask import Blueprint, request, jsonify, current_app
from services.movimentosServices import retornar_movimentos
import calendar

# Import our refactored services and utils
from app.utils.data_transformers import condense_movements
from app.services.financial_service import analyze_movements, calculate_client_metrics
from app.services.llm_service import LLMAnalysisService

bp = Blueprint('repasses', __name__, url_prefix='/v1/repasses')

@bp.route('/comparativo-prestacao-contas', methods=['POST'])
def comparativo_prestacao_contas():
    """
    Endpoint for comparing accounting statements between current and previous months
    """
    current_app.logger.info("Iniciando comparativo de prestação de contas")
    
    data = request.get_json()
    codigo_proprietario = data.get('codigo_proprietario')
    mes_referencia = data.get('mes_referencia')  # formato: "YYYY-MM"
    
    usar_ia_real = data.get('usar_ia_real', False)
    retornar_movimentos_condensados = data.get('retornar_movimentos_condensados', False)
    retornar_movimentos_originais = data.get('retornar_movimentos_originais', False)

    current_app.logger.debug(f"Parâmetros recebidos: código_proprietario={codigo_proprietario}, mes_referencia={mes_referencia}, usar_ia_real={usar_ia_real}")

    if not codigo_proprietario or not mes_referencia:
        current_app.logger.error(f"Parâmetros inválidos: código_proprietario={codigo_proprietario}, mes_referencia={mes_referencia}")
        return jsonify({
            'erro': 'Parâmetros inválidos. É necessário fornecer codigo_proprietario e mes_referencia.'
        }), 400
    
    try:
        # Parse do mês de referência
        year, month = map(int, mes_referencia.split('-'))
        
        # Cálculo do mês anterior
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        
        # Datas de início e fim para o mês atual
        start_date_current = f"{year}-{month:02d}-01"
        last_day_current = calendar.monthrange(year, month)[1]
        end_date_current = f"{year}-{month:02d}-{last_day_current}"
        
        # Datas de início e fim para o mês anterior
        start_date_prev = f"{prev_year}-{prev_month:02d}-01"
        last_day_prev = calendar.monthrange(prev_year, prev_month)[1]
        end_date_prev = f"{prev_year}-{prev_month:02d}-{last_day_prev}"
        
        current_app.logger.info(f"Buscando dados do mês atual: {start_date_current} a {end_date_current}")
        # Fetch data from API
        current_month_data = fetch_movement_data(
            codigo_proprietario, 
            start_date_current, 
            end_date_current
        )
        
        current_app.logger.info(f"Buscando dados do mês anterior: {start_date_prev} a {end_date_prev}")
        previous_month_data = fetch_movement_data(
            codigo_proprietario, 
            start_date_prev, 
            end_date_prev
        )
        
        # Store original data for non-condensed response
        original_current_data = current_month_data
        original_previous_data = previous_month_data
        
        current_app.logger.debug("Condensando movimentos para análise")
        # Process data - always condense for analysis purposes
        condensed_current_data = condense_movements(current_month_data)
        condensed_previous_data = condense_movements(previous_month_data)
        
        current_app.logger.debug("Realizando análise geral dos movimentos")
        # Get overall financial analysis
        overall_analysis = analyze_movements(condensed_current_data, condensed_previous_data)
        
        current_app.logger.info(f"Criando análises por cliente com IA {'real' if usar_ia_real else 'simulada'}")
        # Create client analyses
        client_analyses = create_client_analyses(
            condensed_current_data, 
            condensed_previous_data, 
            usar_ia_real
        )
        
        # Prepare response with appropriate data format based on parameter
        response = {
            'analises_por_cliente': client_analyses,
            'analise_geral': overall_analysis,
            'metricas_financeiras': {
                'total_mes_atual': overall_analysis["total_mes_atual"],
                'total_mes_anterior': overall_analysis["total_mes_anterior"],
                'variacao_absoluta': overall_analysis["variacao_absoluta"],
                'variacao_percentual': overall_analysis["variacao_percentual"],
                'variacao_descricao': overall_analysis["variacao_descricao"]
            },
            'meta': {
                'data_pagamento_repasse': client_analyses[0]['dados_atuais'].get('data_pagamento_repasse') if client_analyses else None,
                'data_vencimento_repasse': client_analyses[0]['dados_atuais'].get('data_vencimento_repasse') if client_analyses else None,
                'mes_referencia': mes_referencia,
                'mes_anterior': f"{prev_year}-{prev_month:02d}",
                'codigo_proprietario': codigo_proprietario,
                'total_clientes': len(client_analyses),
                'tipo_analise': 'ia_real' if usar_ia_real else 'simulada',
            }
        }
        
        # Add movements data based on condensation preference
        if retornar_movimentos_condensados:
            current_app.logger.debug("Incluindo movimentos condensados na resposta")
            response['movimentos_mes_atual_condensados'] = condensed_current_data
            response['movimentos_mes_anterior_condensados'] = condensed_previous_data
        if retornar_movimentos_originais:
            current_app.logger.debug("Incluindo movimentos originais na resposta")
            response['movimentos_mes_atual_originais'] = original_current_data
            response['movimentos_mes_anterior_originais'] = original_previous_data

        current_app.logger.info(f"Comparativo de prestação de contas concluído com sucesso para proprietário {codigo_proprietario}")
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no processamento do comparativo: {str(e)}", exc_info=True)
        return jsonify({'erro': f"Erro ao processar requisição: {str(e)}"}), 500


def fetch_movement_data(codigo_cliente, data_inicial, data_final):
    """
    Fetch movement data from the API and handle potential errors
    """
    current_app.logger.debug(f"Buscando movimentos para cliente {codigo_cliente} entre {data_inicial} e {data_final}")
    
    response = retornar_movimentos(
        numeroPagina=1, 
        numeroRegistros=1000,
        codigoCliente=codigo_cliente,
        dataVencimentoInicial=data_inicial,
        dataVencimentoFinal=data_final
    )
    
    # Check for errors in API response
    if response.get('erro'):
        current_app.logger.error(f"Erro na API externa ao buscar movimentos: {response['erro']}")
        raise Exception(f"Erro ao buscar movimentos: {response['erro']}")
    
    current_app.logger.debug(f"Dados de movimentos recuperados com sucesso para cliente {codigo_cliente}")
    # Process the response
    return response['dados'].json()


def create_client_analyses(condensed_current_data, condensed_previous_data, use_real_llm):
    """
    Create analyses for each client
    """
    current_app.logger.debug("Iniciando criação de análises por cliente")
    
    # Group current data by client name
    current_clients = {}
    for item in condensed_current_data.get('lista', []):
        client_name = item.get('cliente', '')
        if client_name not in current_clients:
            current_clients[client_name] = []
        current_clients[client_name].append(item)
    
    # Group previous data by client name
    previous_clients = {}
    for item in condensed_previous_data.get('lista', []):
        client_name = item.get('cliente', '')
        if client_name not in previous_clients:
            previous_clients[client_name] = []
        previous_clients[client_name].append(item)
    
    current_app.logger.info(f"Dados agrupados para {len(current_clients)} clientes")
    
    # List to store client analyses
    client_analyses = []
    
    # Process each unique client
    for client_name, client_movements in current_clients.items():
        current_app.logger.debug(f"Processando análise para cliente: {client_name}")
        
        # Merge the client's data from all movements
        merged_current_data = merge_client_movements(client_movements)
        
        # Get previous month data if available
        previous_movements = previous_clients.get(client_name, [])
        merged_previous_data = merge_client_movements(previous_movements) if previous_movements else None
        
        # Calculate metrics
        metrics = calculate_client_metrics(merged_current_data, merged_previous_data)
        
        current_app.logger.debug(f"Obtendo insights via LLM para cliente: {client_name}")
        # Get insights based on financial metrics
        insights_text = LLMAnalysisService.get_client_insights(
            client_name,
            merged_current_data,
            merged_previous_data,
            metrics,
            use_real_llm
        )
        
        # Create copies of data without redundant client field
        dados_atuais = {k: v for k, v in merged_current_data.items() if k != 'cliente'}
        dados_anteriores = None
        if merged_previous_data:
            dados_anteriores = {k: v for k, v in merged_previous_data.items() if k != 'cliente'}

        # Add analysis to results
        client_analyses.append({
            'cliente': client_name,
            'dados_atuais': dados_atuais,
            'dados_anteriores': dados_anteriores,
            'metricas_financeiras': metrics,
            'insights_llm': insights_text
        })
        
        current_app.logger.debug(f"Análise concluída para cliente: {client_name}")
    
    current_app.logger.info(f"Total de {len(client_analyses)} análises de clientes criadas")
    return client_analyses

def merge_client_movements(movements):
    """
    Merges multiple movements for a single client into one consolidated record
    """
    if not movements:
        return {}
    
    # Start with the first movement as base
    merged_data = movements[0].copy()
    
    # Initialize datos_resumo as a list if multiple movements exist
    if len(movements) > 1:
        merged_data['dados_resumo'] = [movement.get('dados_resumo', {}) for movement in movements]
    
    return merged_data