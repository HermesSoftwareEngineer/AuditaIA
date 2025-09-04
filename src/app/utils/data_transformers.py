def convert_br_to_float(value):
    """
    Converte um valor numérico em formato brasileiro/europeu para float.
    Trata tanto vírgula como separador decimal quanto ponto como separador de milhares.
    
    Args:
        value: O valor em string para converter ou um valor numérico
        
    Returns:
        float: O valor convertido para float
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if not value:
        return 0.0
    
    if isinstance(value, str):
        # Replace comma with dot for decimal separator
        return float(value.replace('.', '').replace(',', '.'))
    
    return 0.0

def condense_movements(movements_data, proprietario):
    """
    Condensa dados de movimentações para minimizar o uso de tokens 
    enquanto preserva informações financeiras relevantes para análise.
    Agrupa movimentações por código de contrato de aluguel para eliminar
    informações redundantes.
    
    Args:
        movements_data (dict): Os dados originais de movimentações
        proprietario (str): O nome do proprietário para comparação
        
    Returns:
        dict: Versão condensada dos dados de movimentações
    """
    if not movements_data:
        return {"lista": [], "quantidade": 0}
    
    # Dicionário para armazenar movimentações por código de contrato
    movements_by_contract = {}
    
    for movement in movements_data.get("lista", []):
        codigo_contrato = movement.get("codigocontratoaluguel", "sem_contrato")
        nome_cliente = movement.get("nomecliente")
        tipo_cliente = movement.get("tipocliente")
        
        # Define o cliente baseado no tipo e no nome
        if tipo_cliente == "Locatário":
            cliente = f"{tipo_cliente} - {nome_cliente}" if nome_cliente else "Locatário desconhecido"
        else:
            if codigo_contrato == 0:
                cliente = f"{tipo_cliente} - {nome_cliente} (Contrato não identificado)"
            else: 
                cliente = f"Contrato {codigo_contrato} (Locatário não encontrado pra esse contrato)"
        
        repasses = movement.get("repasses", [])
        data_pagamento_repasse = None
        data_vencimento_repasse = None

        # Busca datas de pagamento e vencimento nos repasses
        for repasse in repasses:
            # Se ainda não tiver data de pagamento, tenta pegar deste repasse
            if data_pagamento_repasse is None:
                data_pagamento_repasse = repasse.get("datapagamento")
            
            # Se ainda não tiver data de vencimento, tenta pegar deste repasse
            if data_vencimento_repasse is None:
                data_vencimento_repasse = repasse.get("datavencimento")
            
            # Se já encontrou ambos os valores, pode parar de procurar
            if data_pagamento_repasse is not None and data_vencimento_repasse is not None:
                break

        codigodetalhe = 0
        # Lista para armazenar os detalhes resumidos
        summary_list = []
        
        # Processa os detalhes da movimentação
        for detail in movement.get("detalhes", []):
            codigodetalhe += 1
            account_name = detail.get("nomeplanoconta", "Outros")
            description = detail.get("descricao", "Outros")
            # Converte valor em formato brasileiro para float
            value = convert_br_to_float(detail.get("valor", 0))
            
            # Adiciona item à lista de resumo
            summary_list.append({
                "codigodetalhe": codigodetalhe,
                "conta": account_name,
                "valor": round(value, 2),
                "descricao": description
            })

        # Remove itens duplicados da lista
        summary_list = remover_duplicados(summary_list)

        # Converte saldo para float se for uma string
        saldo = movement.get("saldo")
        if saldo and isinstance(saldo, str):
            saldo = convert_br_to_float(saldo)
            
        # Cria ou atualiza a entrada do contrato
        if codigo_contrato in movements_by_contract:
            # Contrato já existe, adiciona à entrada existente
            existing_entry = movements_by_contract[codigo_contrato]
                
            # Adiciona os detalhes financeiros ao resumo existente
            for summary_item in summary_list:
                existing_entry["detalhes_resumo"].append(summary_item)
                    
            # Atualiza o saldo total
            if existing_entry["saldo"] is not None and saldo is not None:
                existing_entry["saldo"] += saldo
                existing_entry["saldo"] = round(existing_entry["saldo"], 2)
                
            # Prioriza Locatários na definição do cliente
            if tipo_cliente == "Locatário":
                existing_entry["cliente"] = cliente
            elif not existing_entry["cliente"]:
                # Usa cliente atual se não houver Locatário definido
                existing_entry["cliente"] = cliente
        else:
            # Cria nova entrada para o contrato
            movements_by_contract[codigo_contrato] = {
                "codigo": movement.get("codigo"),
                "data_vencimento_cliente": movement.get("datavencimento"),
                "data_pagamento_cliente": movement.get("datapagamento"),
                "saldo": saldo,
                "detalhes_resumo": summary_list,
                "cliente": cliente,
                "data_pagamento_repasse": data_pagamento_repasse,
                "data_vencimento_repasse": data_vencimento_repasse
            }
    
    # Converte o dicionário para lista de valores
    condensed_list = list(movements_by_contract.values())
    
    return {
        "lista": condensed_list,
        "quantidade": len(condensed_list)
    }

def remover_duplicados(movimentos):
    """
    Remove movimentações duplicadas da lista
    
    Args:
        movimentos: Lista de movimentações para verificar
        
    Returns:
        list: Lista de movimentações sem duplicações
    """
    seen = set()
    unique_movements = []
    
    for movimento in movimentos:
        # Verifica se o movimento tem um código de detalhe para usar como identificador
        if isinstance(movimento, dict) and 'codigodetalhe' in movimento:
            identificador = movimento['codigodetalhe']
            if identificador not in seen:
                seen.add(identificador)
                unique_movements.append(movimento)
        else:
            # Se não tiver código de detalhe, mantém a entrada original
            # Usa um hash do objeto inteiro como identificador
            movement_repr = str(movimento)
            if movement_repr not in seen:
                seen.add(movement_repr)
                unique_movements.append(movimento)
            
    return unique_movements