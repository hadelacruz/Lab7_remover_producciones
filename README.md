# Simplificador de Gramáticas - Eliminación de Producciones Epsilon

Este programa implementa un algoritmo para eliminar producciones epsilon (ε) de gramáticas libres de contexto.

## Video Demostrativo

<p align="center">
  <a href="https://www.youtube.com/watch?v=UaxwvCaheGs">
    <img src="https://img.youtube.com/vi/UaxwvCaheGs/0.jpg" alt="Video Demostrativo Lab 7 TC">
  </a>
</p>

> [!IMPORTANT]
> En la carpeta `problema-2/` se encuentra el documento PDF que contiene la resolución del problema 2.

## Gramáticas de ejemplo

### Gramática 1:
```
S -> 0A0 | 1B1 | BB
A -> C
B -> S | A
C -> S | ε
```

### Gramática 2:
```
S -> aAa | bBb | ε
A -> C | a
B -> C | b
C -> CDE | ε
D -> A | B | ab
```

### Gramática 3:
```
S -> ASA | aB
A -> B | S
B -> b | ε
```

## Funcionalidades

1. **Validación de formato**: Utiliza expresiones regulares para validar que cada línea del archivo tenga el formato correcto de una producción.

2. **Análisis de símbolos anulables**: Encuentra todos los símbolos que pueden derivar en epsilon (ε).

3. **Generación de nuevas producciones**: Para cada producción con símbolos anulables, genera todas las 2^m combinaciones posibles.

4. **Eliminación de producciones ε**: Remueve todas las producciones epsilon y muestra la gramática resultante.

## Uso

```bash
python main.py
```

El programa procesará automáticamente los tres archivos de gramática (`grammar1.txt`, `grammar2.txt` y `grammar3.txt`) y mostrará:

- El proceso de parsing y validación
- La gramática original cargada
- El algoritmo paso a paso para encontrar símbolos anulables
- La generación de nuevas producciones
- La gramática final sin producciones epsilon

## Formato de archivos de gramática

- Cada línea representa una o más producciones para un no-terminal
- Formato: `No-terminal -> producción1 | producción2 | ... | ε`
- Letras mayúsculas: No-terminales
- Letras minúsculas y números: Terminales
- `ε`: Simboliza la cadena vacía
- `|`: Operador OR para separar producciones alternativas

## Algoritmo implementado

1. **Encontrar símbolos anulables**:
   - Símbolos que producen ε directamente
   - Símbolos cuyas producciones consisten únicamente de símbolos anulables

2. **Generar nuevas producciones**:
   - Para cada producción con m símbolos anulables
   - Generar 2^m producciones considerando todas las combinaciones
   - Eliminar producciones vacías (excepto ε original)

3. **Construcción de gramática final**:
   - Reemplazar producciones originales con las nuevas
   - Eliminar todas las producciones ε
   - Mantener producciones únicas

## Ejemplo de salida

El programa muestra el proceso completo paso a paso, incluyendo:
- Validación de cada línea
- Identificación de símbolos anulables por iteraciones
- Generación de nuevas producciones para cada no-terminal
- Gramática final sin producciones epsilon
