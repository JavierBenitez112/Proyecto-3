"""
Parser para archivos YAML de configuración de Máquinas de Turing
"""

import yaml
from typing import Dict, Any


def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    """
    Parsea un archivo YAML con la configuración de una MT
    
    Args:
        file_path: Ruta al archivo YAML
        
    Returns:
        Diccionario con la configuración parseada
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    # Validar estructura básica
    if 'q_states' not in config:
        raise ValueError("El archivo YAML debe contener 'q_states'")
    if 'alphabet' not in config:
        raise ValueError("El archivo YAML debe contener 'alphabet'")
    if 'tape_alphabet' not in config:
        raise ValueError("El archivo YAML debe contener 'tape_alphabet'")
    if 'delta' not in config:
        raise ValueError("El archivo YAML debe contener 'delta'")
    
    return config


