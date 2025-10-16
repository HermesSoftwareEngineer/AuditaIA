from flask import Blueprint, request, jsonify, current_app
from services.movimentosServices import retornar_movimentos
import calendar
from services.clienteServices import pesquisar_cliente

# Importação dos nossos serviços e utilitários refatorados
from app.utils.data_transformers import condense_movements
from app.services.financial_service import analyze_movements, calculate_client_metrics
from app.services.llm_service import LLMAnalysisService

bp = Blueprint('repasses', __name__, url_prefix='/v1/repasses')

@bp.route('/comparativo-prestacao-contas', methods=['POST'])
def comparativo_prestacao_contas():
    """
    Endpoint para comparação de prestações de contas entre mês atual e anterior
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

        proprietarioInfo = pesquisar_cliente(codigo_proprietario)
        proprietario = proprietarioInfo.get("dados").json().get("nome") if not proprietarioInfo.get("erro") else None
        
        # Store original data for non-condensed response
        original_current_data = current_month_data
        original_previous_data = previous_month_data
        
        current_app.logger.debug("Condensando movimentos para análise")
        # Process data - always condense for analysis purposes
        condensed_current_data = condense_movements(current_month_data, proprietario)
        condensed_previous_data = condense_movements(previous_month_data, proprietario)

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
    Busca dados de movimentação da API e trata possíveis erros
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
    Cria análises para cada cliente com base nos dados financeiros atuais e anteriores
    
    Args:
        condensed_current_data: Dados do mês atual condensados
        condensed_previous_data: Dados do mês anterior condensados
        use_real_llm: Flag indicando se deve usar IA real ou simulada
        
    Returns:
        list: Lista com análises por cliente
    """
    analyses_results = []

    # Cria um dicionário de contratos do mês anterior para lookup rápido
    contracts_previous_month = {}
    for item in condensed_previous_data.get('lista', []):
        codigo_contrato = item.get('codigo')
        if codigo_contrato:
            contracts_previous_month[codigo_contrato] = item

    # Processa clientes do mês atual
    for item in condensed_current_data.get('lista', []):
        client_name = item.get('cliente')
        codigo_contrato = item.get('codigo')

        dados_atuais = {
            "codigo_contrato": codigo_contrato,
            "data_pagamento_cliente": item.get("data_pagamento_cliente"),
            "data_pagamento_repasse": item.get("data_pagamento_repasse"),
            "data_vencimento_cliente": item.get("data_vencimento_cliente"),
            "data_vencimento_repasse": item.get("data_vencimento_repasse"),
            "detalhes_resumo": item.get("detalhes_resumo"),
            "saldo": item.get("saldo")
        }

        # Busca dados anteriores pelo código do contrato
        if codigo_contrato and codigo_contrato in contracts_previous_month:
            previous_item = contracts_previous_month[codigo_contrato]
            dados_anteriores = {
                "codigo_contrato": codigo_contrato,
                "data_pagamento_cliente": previous_item.get("data_pagamento_cliente"),
                "data_pagamento_repasse": previous_item.get("data_pagamento_repasse"),
                "data_vencimento_cliente": previous_item.get("data_vencimento_cliente"),
                "data_vencimento_repasse": previous_item.get("data_vencimento_repasse"),
                "detalhes_resumo": previous_item.get("detalhes_resumo"),
                "saldo": previous_item.get("saldo")
            }
        else:
            dados_anteriores = {}

        # Calcula as métricas usando a função calculate_client_metrics
        metrics = calculate_client_metrics(dados_atuais, dados_anteriores) 
        
        # Gerar insights com IA apenas se houver diferença entre os saldos
        insights = ""
        if metrics.get("diferenca") != 0:
            try:
                insights = LLMAnalysisService.get_client_insights(
                    client_name,
                    dados_atuais,
                    dados_anteriores,
                    metrics,
                    use_real_llm
                )
            except Exception as e:
                current_app.logger.error(f"Erro ao gerar insights: {str(e)}")
                insights = "Não foi possível gerar insights com IA. Erro no processamento."

        client_analysis = {
            'cliente': client_name,
            'codigo_contrato': codigo_contrato,
            'dados_atuais': dados_atuais,
            'dados_anteriores': dados_anteriores,
            'metricas_financeiras': metrics,
            'insights_llm': insights
        }
        
        analyses_results.append(client_analysis)

    return analyses_results