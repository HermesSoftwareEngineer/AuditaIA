"""
Utility functions for data transformation operations
"""

def convert_br_to_float(value):
    """
    Convert a Brazilian/European formatted number string to float.
    Handles both comma as decimal separator and dot as thousands separator.
    
    Args:
        value: The string value to convert or a numeric value
        
    Returns:
        float: The converted float value
    """
    if isinstance(value, (int, float)):
        return float(value)
    
    if not value:
        return 0.0
    
    if isinstance(value, str):
        # Replace comma with dot for decimal separator
        return float(value.replace('.', '').replace(',', '.'))
    
    return 0.0


def condense_movements(movements_data):
    """
    Condense movement data to minimize token usage while preserving 
    relevant financial information for AI analysis.
    Groups movements by client to eliminate redundant information.
    
    Args:
        movements_data (dict): The original movements data
        
    Returns:
        dict: Condensed version of the movements data
    """
    if not movements_data:
        return {"lista": [], "quantidade": 0}
    
    # Dictionary to store movements by client
    movements_by_client = {}
    
    for movement in movements_data.get("lista", []):
        cliente = movement.get("nomecliente")
        
        for repasse in movement.get("repasses", []):
            data_pagamento_repasse = repasse.get("datapagamento")
            data_vencimento_repasse = repasse.get("datavencimento")

        codigodetalhe = 0
        # Process movement details to aggregate by account type
        details_summary = {}
        for detail in movement.get("detalhes", []):
            codigodetalhe += 1
            account_name = detail.get("nomeplanoconta", "Outros")
            description = detail.get("descricao", "Outros")
            # Safely convert Brazilian number format to float
            value = convert_br_to_float(detail.get("valor", 0))
            details_summary[codigodetalhe] = [account_name, value, description]

        # Convert summary dict to list of simplified items
        summary_list = [
            {"codigodetalhe": key, "conta": value[0], "valor": round(value[1], 2), "descricao": value[2]} 
            for key, value in details_summary.items()
        ]

        summary_list = remover_duplicados(summary_list)

        # Convert saldo from Brazilian format if it's a string
        saldo = movement.get("saldo")
        if saldo and isinstance(saldo, str):
            saldo = convert_br_to_float(saldo)
            
        # Create or update client entry
        if cliente in movements_by_client:
            # Client already exists, add to existing entry
            existing_entry = movements_by_client[cliente]
                
            # Add historical context
            # existing_entry["historicos"].append(movement.get("historico"))
                
            # Merge financial details
            for summary_item in summary_list:
                existing_entry["detalhes_resumo"].append(summary_item)
                    
            # Update total saldo
            if existing_entry["saldo"] is not None and saldo is not None:
                existing_entry["saldo"] += saldo
                existing_entry["saldo"] = round(existing_entry["saldo"], 2)
        else:
            # New client, create new entry
            movements_by_client[cliente] = {
                "codigo": movement.get("codigo"),
                "data_vencimento_cliente": movement.get("datavencimento"),
                "data_pagamento_cliente": movement.get("datapagamento"),
                "saldo": saldo,
                "detalhes_resumo": summary_list,
                "cliente": cliente,
                "data_pagamento_repasse": data_pagamento_repasse,
                "data_vencimento_repasse": data_vencimento_repasse
                }
    
    # Convert dictionary back to list
    condensed_list = list(movements_by_client.values())
    
    return {
        "lista": condensed_list,
        "quantidade": len(condensed_list)
    }

def remover_duplicados(movimentos):
    """
    Remove duplicate movements from the list
    """
    seen = set()
    unique_movements = []
    
    for movimento in movimentos:
        # Check if this movement has a 'codigodetalhe' to use as identifier
        if isinstance(movimento, dict) and 'codigodetalhe' in movimento:
            identificador = movimento['codigodetalhe']
            if identificador not in seen:
                seen.add(identificador)
                unique_movements.append(movimento)
        else:
            # If there's no 'codigodetalhe', keep the original entry
            # Use a hash of the entire object as an identifier
            movement_repr = str(movimento)
            if movement_repr not in seen:
                seen.add(movement_repr)
                unique_movements.append(movimento)
            
    return unique_movements