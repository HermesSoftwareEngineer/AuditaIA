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
    current_app.logger.debug("Iniciando criação de análises por cliente")
    
    # Extrair lista de itens dos dados condensados
    current_items = condensed_current_data.get('lista', [])
    previous_items = condensed_previous_data.get('lista', [])
    
    # Organizar os dados por cliente
    current_by_client = {}
    previous_by_client = {}
    
    # Agrupar dados atuais por cliente
    for item in current_items:
        client_name = item.get('cliente', '')
        if not client_name:
            continue
            
        if client_name not in current_by_client:
            current_by_client[client_name] = []
        current_by_client[client_name].append(item)
    
    # Agrupar dados do mês anterior por cliente
    for item in previous_items:
        client_name = item.get('cliente', '')
        if not client_name:
            continue
            
        if client_name not in previous_by_client:
            previous_by_client[client_name] = []
        previous_by_client[client_name].append(item)
    
    current_app.logger.info(f"Dados agrupados para {len(current_by_client)} clientes")
    
    # Lista para armazenar os resultados das análises
    analyses_results = []
    
    # Processar cada cliente
    for client_name, client_items in current_by_client.items():
        current_app.logger.debug(f"Analisando dados para cliente: {client_name}")
        
        # Mesclar dados do mês atual
        merged_current = merge_client_movements(client_items)
        
        # Obter e mesclar dados do mês anterior se disponíveis
        previous_items_for_client = previous_by_client.get(client_name, [])
        merged_previous = merge_client_movements(previous_items_for_client) if previous_items_for_client else None
        
        # Calcular métricas financeiras
        metrics = calculate_client_metrics(merged_current, merged_previous)
        
        current_app.logger.debug(f"Gerando insights via LLM para cliente: {client_name}")
        # Obter insights via LLM
        insights = LLMAnalysisService.get_client_insights(
            client_name,
            merged_current,
            merged_previous,
            metrics,
            use_real_llm
        )
        
        # Remover campo cliente redundante dos dados mesclados
        dados_atuais = {k: v for k, v in merged_current.items() if k != 'cliente'}
        dados_anteriores = None
        if merged_previous:
            dados_anteriores = {k: v for k, v in merged_previous.items() if k != 'cliente'}
        
        # Criar objeto de análise para este cliente
        client_analysis = {
            'cliente': client_name,
            'dados_atuais': dados_atuais,
            'dados_anteriores': dados_anteriores,
            'metricas_financeiras': metrics,
            'insights_llm': insights
        }
        
        analyses_results.append(client_analysis)
        current_app.logger.debug(f"Análise concluída para cliente: {client_name}")
    
    current_app.logger.info(f"Total de {len(analyses_results)} análises de clientes criadas")
    return analyses_results


def merge_client_movements(movements):
    """
    Mescla os movimentos de um cliente, consolidando por contrato
    
    Args:
        movements: Lista de movimentos de um cliente
        
    Returns:
        dict: Dados mesclados do cliente
    """
    if not movements or len(movements) == 0:
        return {}
    
    # Se houver apenas um movimento, retorna diretamente
    if len(movements) == 1:
        return movements[0].copy()
    
    # Agrupar movimentos por código de contrato (se existir)
    contracts = {}
    for movement in movements:
        # Usar um identificador único para cada contrato, usando um valor padrão se não existir
        contract_id = movement.get('codigo', 'sem_codigo')
        
        if contract_id not in contracts:
            contracts[contract_id] = []
        
        contracts[contract_id].append(movement)
    
    # Criar dados consolidados
    result = movements[0].copy()
    
    # Consolidar detalhes de resumo
    all_details = []
    for movement in movements:
        details = movement.get('detalhes_resumo', [])
        all_details.extend(details)
    
    # Remover possíveis duplicatas nos detalhes (baseado no código do detalhe)
    unique_details = {}
    for detail in all_details:
        detail_code = detail.get('codigodetalhe')
        if detail_code and detail_code not in unique_details:
            unique_details[detail_code] = detail
    
    # Substituir os detalhes originais pelos consolidados
    result['detalhes_resumo'] = list(unique_details.values()) if unique_details else all_details
    
    # Calcular saldo total
    total_balance = sum(movement.get('saldo', 0) for movement in movements)
    result['saldo'] = total_balance
    
    # Caso existam múltiplos contratos, adicionar informação de contratos consolidados
    if len(contracts) > 1:
        result['contratos_consolidados'] = len(contracts)
        result['codigos_contratos'] = list(contracts.keys())
    
    # Garantir que as informações de cliente e datas sejam consistentes
    result['cliente'] = movements[0].get('cliente', '')
    
    # Usar as datas mais recentes disponíveis
    valid_dates = [m.get('data_pagamento_repasse') for m in movements if m.get('data_pagamento_repasse')]
    if valid_dates:
        result['data_pagamento_repasse'] = max(valid_dates)
    
    valid_dates = [m.get('data_vencimento_repasse') for m in movements if m.get('data_vencimento_repasse')]
    if valid_dates:
        result['data_vencimento_repasse'] = max(valid_dates)
    
    return result