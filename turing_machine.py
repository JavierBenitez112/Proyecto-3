"""
Simulador de Máquinas de Turing
Implementa la lógica para simular una MT de una cinta
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Transition:
    """Representa una transición de la MT"""
    initial_state: str
    mem_cache_value: Optional[str]  # Puede ser None (blank)
    tape_input: str
    final_state: str
    new_mem_cache_value: Optional[str]  # Puede ser None (blank)
    tape_output: Optional[str]  # Puede ser None (blank)
    tape_displacement: str  # 'L', 'R', o 'S'


class TuringMachine:
    """Clase que representa una Máquina de Turing"""
    
    def __init__(self, config: dict):
        """
        Inicializa la MT desde un diccionario de configuración
        
        Args:
            config: Diccionario con la configuración de la MT
        """
        # Estados
        self.states = config['q_states']['q_list']
        self.initial_state = config['q_states']['initial']
        self.final_state = config['q_states']['final']
        
        # Alfabetos
        self.alphabet = config['alphabet']
        self.tape_alphabet = config['tape_alphabet']
        
        # Función de transición
        self.transitions: List[Transition] = []
        for delta_item in config['delta']:
            params = delta_item['params']
            output = delta_item['output']
            
            # Manejar valores null/None de YAML
            mem_cache_in = params.get('mem_cache_value')
            if mem_cache_in is None or mem_cache_in == '':
                mem_cache_in = None
            
            tape_input = params['tape_input']
            # Si tape_input es None o string vacío, representa blank
            if tape_input is None or tape_input == '':
                tape_input = None
            
            mem_cache_out = output.get('mem_cache_value')
            if mem_cache_out is None or mem_cache_out == '':
                mem_cache_out = None
            
            tape_output = output.get('tape_output')
            if tape_output is None or tape_output == '':
                tape_output = None
            
            transition = Transition(
                initial_state=params['initial_state'],
                mem_cache_value=mem_cache_in,
                tape_input=tape_input,
                final_state=output['final_state'],
                new_mem_cache_value=mem_cache_out,
                tape_output=tape_output,
                tape_displacement=output['tape_displacement']
            )
            self.transitions.append(transition)
        
        # Cadenas a simular
        self.simulation_strings = config.get('simulation_strings', [])
    
    def find_transition(self, state: str, mem_cache: Optional[str], tape_symbol: Optional[str]) -> Optional[Transition]:
        """
        Busca una transición aplicable dado el estado actual, memoria y símbolo de la cinta
        
        Args:
            state: Estado actual
            mem_cache: Valor en memoria/caché (puede ser None)
            tape_symbol: Símbolo leído de la cinta (None representa blank)
            
        Returns:
            Transición aplicable o None si no hay ninguna
        """
        # Convertir None a string vacío o manejar blank según la configuración
        # En YAML, blank puede ser null, None, o string vacío
        tape_input = tape_symbol if tape_symbol is not None else None
        
        for transition in self.transitions:
            # Comparar estado y memoria
            if transition.initial_state != state:
                continue
            if transition.mem_cache_value != mem_cache:
                continue
            
            # Comparar símbolo de cinta (manejar blank)
            transition_input = transition.tape_input
            # Si la transición tiene None o string vacío, representa blank
            if transition_input is None or transition_input == '':
                transition_input = None
            
            if transition_input == tape_input:
                return transition
        
        return None
    
    def simulate(self, input_string: str) -> Tuple[List[str], bool]:
        """
        Simula la ejecución de la MT con una cadena de entrada
        
        Args:
            input_string: Cadena de entrada a simular
            
        Returns:
            Tupla con (lista de descripciones instantáneas, aceptada)
        """
        # Inicializar cinta: convertir la cadena en lista de símbolos
        tape = list(input_string)
        tape_position = 0
        current_state = self.initial_state
        mem_cache = None  # Memoria/caché inicial
        
        # Lista de descripciones instantáneas
        instant_descriptions = []
        
        # Agregar descripción instantánea inicial
        id_str = self._create_instant_description(tape, tape_position, current_state, mem_cache)
        instant_descriptions.append(id_str)
        
        max_steps = 10000  # Límite de pasos para evitar bucles infinitos
        step = 0
        
        while step < max_steps:
            # Leer símbolo actual de la cinta
            if tape_position < 0:
                # Extender cinta hacia la izquierda con blank
                tape.insert(0, None)  # None representa blank
                tape_position = 0
            elif tape_position >= len(tape):
                # Extender cinta hacia la derecha con blank
                tape.append(None)
            
            current_symbol = tape[tape_position] if tape[tape_position] is not None else None
            
            # Buscar transición aplicable
            transition = self.find_transition(current_state, mem_cache, current_symbol)
            
            if transition is None:
                # No hay transición aplicable
                break
            
            # Aplicar transición
            current_state = transition.final_state
            mem_cache = transition.new_mem_cache_value
            
            # Escribir en la cinta
            if transition.tape_output is not None:
                tape[tape_position] = transition.tape_output
            else:
                tape[tape_position] = None  # Blank
            
            # Mover cabeza de la cinta
            if transition.tape_displacement == 'L':
                tape_position -= 1
            elif transition.tape_displacement == 'R':
                tape_position += 1
            # 'S' significa Stay, no movemos
            
            # Agregar descripción instantánea
            id_str = self._create_instant_description(tape, tape_position, current_state, mem_cache)
            instant_descriptions.append(id_str)
            
            # Verificar si llegamos al estado final
            if current_state == self.final_state:
                return instant_descriptions, True
            
            step += 1
        
        # Si salimos del bucle, la cadena no fue aceptada
        return instant_descriptions, False
    
    def _create_instant_description(self, tape: List[Optional[str]], 
                                     position: int, 
                                     state: str, 
                                     mem_cache: Optional[str]) -> str:
        """
        Crea una descripción instantánea (ID) de la configuración actual
        
        Formato: [estado, mem_cache] símbolo_actual resto_de_la_cinta
        
        Args:
            tape: Lista que representa la cinta
            position: Posición de la cabeza de lectura/escritura
            state: Estado actual
            mem_cache: Valor en memoria/caché
            
        Returns:
            String con la descripción instantánea
        """
        # Construir la parte del estado y memoria
        state_part = f"[{state}"
        if mem_cache is not None:
            state_part += f",{mem_cache}"
        state_part += "]"
        
        # Asegurar que la posición esté dentro de los límites de la cinta
        if position < 0:
            # La cabeza está a la izquierda de la cinta
            return state_part + "B" + "".join(self._symbol_to_str(s) for s in tape)
        elif position >= len(tape):
            # La cabeza está a la derecha de la cinta
            return "".join(self._symbol_to_str(s) for s in tape) + state_part + "B"
        else:
            # La cabeza está dentro de la cinta
            left_part = "".join(self._symbol_to_str(s) for s in tape[:position])
            current_symbol = self._symbol_to_str(tape[position])
            right_part = "".join(self._symbol_to_str(s) for s in tape[position+1:])
            return left_part + state_part + current_symbol + right_part
    
    def _symbol_to_str(self, symbol: Optional[str]) -> str:
        """
        Convierte un símbolo a string, manejando blank
        
        Args:
            symbol: Símbolo (None representa blank)
            
        Returns:
            String representando el símbolo
        """
        if symbol is None:
            return "B"  # B representa blank
        return symbol

