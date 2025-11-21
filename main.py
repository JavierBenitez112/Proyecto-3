"""
Script principal para el simulador de Máquinas de Turing
"""

import sys
import argparse
from turing_machine import TuringMachine
from yaml_parser import parse_yaml_file


def main():
    """Función principal del simulador"""
    parser = argparse.ArgumentParser(
        description='Simulador de Máquinas de Turing',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'yaml_file',
        type=str,
        help='Ruta al archivo YAML con la configuración de la MT'
    )
    
    args = parser.parse_args()
    
    try:
        # Parsear archivo YAML
        print(f"Cargando configuración desde: {args.yaml_file}")
        config = parse_yaml_file(args.yaml_file)
        
        # Crear Máquina de Turing
        tm = TuringMachine(config)
        print(f"MT creada exitosamente")
        print(f"Estados: {tm.states}")
        print(f"Estado inicial: {tm.initial_state}")
        print(f"Estado final: {tm.final_state}")
        print(f"Alfabeto: {tm.alphabet}")
        print(f"Alfabeto de cinta: {tm.tape_alphabet}")
        print(f"Transiciones: {len(tm.transitions)}")
        print(f"Cadenas a simular: {len(tm.simulation_strings)}")
        print("\n" + "="*80 + "\n")
        
        # Simular cada cadena
        for i, input_string in enumerate(tm.simulation_strings, 1):
            print(f"Simulación {i}: Cadena de entrada: '{input_string}'")
            print("-" * 80)
            
            instant_descriptions, accepted = tm.simulate(input_string)
            
            # Mostrar todas las descripciones instantáneas
            for step, id_str in enumerate(instant_descriptions):
                print(f"Paso {step}: {id_str}")
            
            # Mostrar resultado
            print("-" * 80)
            if accepted:
                print(f"RESULTADO: La cadena '{input_string}' fue ACEPTADA")
            else:
                print(f"RESULTADO: La cadena '{input_string}' fue RECHAZADA")
            
            print("\n" + "="*80 + "\n")
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.yaml_file}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error al parsear el archivo YAML: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error en la configuración: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

main()


