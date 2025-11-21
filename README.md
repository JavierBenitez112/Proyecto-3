# Simulador de Máquinas de Turing

Simulador de Máquinas de Turing (MT) de una cinta que carga la descripción formal desde un archivo YAML y simula cadenas de entrada.

## Requisitos

- Python 3.7 o superior
- PyYAML

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py <archivo_yaml>
```

Ejemplo:
```bash
python main.py example_mt_1.yaml
```

## Estructura del Archivo YAML

El archivo YAML debe contener: `q_states` (estados inicial y final), `alphabet`, `tape_alphabet`, `delta` (transiciones) y `simulation_strings` (cadenas a simular). El símbolo blank se representa como `null` en YAML.
