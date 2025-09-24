import re
import itertools
from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple

class GrammarSimplifier:
    def __init__(self):
        self.productions = defaultdict(list)  # Dict[str, List[str]]
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = None
        
    def validate_production_line(self, line: str) -> bool:
        """
        Valida que una línea de producción tenga el formato correcto.
        Regex mejorada para validar producciones de gramáticas libres de contexto.
        """
        # Eliminar espacios en blanco al inicio y final
        line = line.strip()
        
        # Línea vacía no es válida
        if not line:
            return False
        
        # Regex para validar producciones
        # Formato: No-terminal -> produccion1 | produccion2 | ... 
        # donde cada producción puede ser ε o una secuencia de terminales/no-terminales
        pattern = r'^[A-Z]\s*->\s*([A-Za-z0-9ε]+(\s*\|\s*[A-Za-z0-9ε]+)*|ε)$'
        
        match = re.match(pattern, line)
        if not match:
            return False
        
        # Verificar que no termine con | o tenga || consecutivos
        right_side = line.split('->', 1)[1].strip()
        if right_side.endswith('|') or '||' in right_side or right_side.startswith('|'):
            return False
        
        return True
    
    def parse_grammar_file(self, filename: str) -> bool:
        """
        Carga y parsea un archivo de gramática.
        Retorna True si el parsing fue exitoso, False en caso contrario.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"\n=== Parseando archivo: {filename} ===")
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:  # Saltar líneas vacías
                    continue
                
                print(f"Línea {i}: {line}")
                
                # Validar formato de la línea
                if not self.validate_production_line(line):
                    print(f"ERROR: Línea {i} tiene formato incorrecto: {line}")
                    return False
                
                # Parsear la producción
                left_side, right_side = line.split('->', 1)
                left_side = left_side.strip()
                right_side = right_side.strip()
                
                # El primer símbolo no-terminal es el símbolo inicial
                if self.start_symbol is None:
                    self.start_symbol = left_side
                
                # Agregar el no-terminal al conjunto
                self.non_terminals.add(left_side)
                
                # Dividir las producciones por el operador OR "|"
                productions = [prod.strip() for prod in right_side.split('|')]
                
                for prod in productions:
                    self.productions[left_side].append(prod)
                    
                    # Identificar terminales y no-terminales en la producción
                    for char in prod:
                        if char.isupper():
                            self.non_terminals.add(char)
                        elif char.islower() or char.isdigit():
                            self.terminals.add(char)
                        # ε no se considera terminal ni no-terminal para este propósito
            
            print("✓ Archivo parseado exitosamente")
            return True
            
        except FileNotFoundError:
            print(f"ERROR: No se pudo encontrar el archivo {filename}")
            return False
        except Exception as e:
            print(f"ERROR al parsear el archivo: {e}")
            return False
    
    def display_grammar(self):
        """Muestra la gramática actual."""
        print("\n=== GRAMÁTICA CARGADA ===")
        print(f"Símbolo inicial: {self.start_symbol}")
        print(f"No-terminales: {sorted(self.non_terminals)}")
        print(f"Terminales: {sorted(self.terminals)}")
        print("\nProducciones:")
        for non_terminal in sorted(self.non_terminals):
            if non_terminal in self.productions:
                productions_str = ' | '.join(self.productions[non_terminal])
                print(f"  {non_terminal} -> {productions_str}")
    
    def find_nullable_symbols(self) -> Set[str]:
        """
        Encuentra todos los símbolos anulables (que pueden derivar en ε).
        Retorna el conjunto de símbolos anulables.
        """
        print("\n=== ENCONTRANDO SÍMBOLOS ANULABLES ===")
        
        nullable = set()
        changed = True
        iteration = 0
        
        while changed:
            changed = False
            iteration += 1
            old_nullable = nullable.copy()
            
            print(f"\nIteración {iteration}:")
            print(f"  Símbolos anulables actuales: {sorted(nullable) if nullable else 'ninguno'}")
            
            for non_terminal, productions in self.productions.items():
                if non_terminal in nullable:
                    continue
                
                for production in productions:
                    # Si la producción es ε, el símbolo es anulable
                    if production == 'ε':
                        nullable.add(non_terminal)
                        changed = True
                        print(f"  {non_terminal} es anulable (produce ε directamente)")
                        break
                    
                    # Si todos los símbolos de la producción son anulables
                    if all(symbol in nullable for symbol in production if symbol.isupper()):
                        if any(symbol.isupper() for symbol in production):  # Solo si tiene no-terminales
                            nullable.add(non_terminal)
                            changed = True
                            print(f"  {non_terminal} es anulable (todos los no-terminales en '{production}' son anulables)")
                            break
        
        print(f"\n✓ Símbolos anulables finales: {sorted(nullable)}")
        return nullable
    
    def generate_new_productions(self, production: str, nullable_symbols: Set[str]) -> List[str]:
        """
        Genera todas las producciones posibles para una producción dada,
        considerando todas las combinaciones de símbolos anulables.
        """
        if production == 'ε':
            return []  # Las producciones ε se eliminan
        
        # Encontrar posiciones de símbolos anulables
        nullable_positions = []
        for i, symbol in enumerate(production):
            if symbol in nullable_symbols:
                nullable_positions.append(i)
        
        if not nullable_positions:
            return [production]  # No hay símbolos anulables
        
        new_productions = set()
        
        # Generar todas las combinaciones posibles (2^m)
        for r in range(len(nullable_positions) + 1):
            for combination in itertools.combinations(nullable_positions, r):
                new_prod = ""
                for i, symbol in enumerate(production):
                    if i not in combination:  # No eliminar este símbolo
                        new_prod += symbol
                
                if new_prod:  # No agregar producciones vacías (excepto ε original)
                    new_productions.add(new_prod)
        
        return list(new_productions)
    
    def remove_epsilon_productions(self):
        """
        Elimina las producciones ε de la gramática.
        Muestra el proceso paso a paso.
        """
        print("\n" + "="*50)
        print("ALGORITMO PARA ELIMINAR PRODUCCIONES EPSILON")
        print("="*50)
        
        # Paso 1: Encontrar símbolos anulables
        nullable_symbols = self.find_nullable_symbols()
        
        if not nullable_symbols:
            print("\n✓ No hay símbolos anulables. La gramática ya no tiene producciones ε.")
            return
        
        # Paso 2: Generar nuevas producciones
        print("\n=== GENERANDO NUEVAS PRODUCCIONES ===")
        new_grammar = defaultdict(list)
        
        for non_terminal, productions in self.productions.items():
            print(f"\nProcesando producciones de {non_terminal}:")
            new_productions_for_nt = set()
            
            for production in productions:
                print(f"  Producción original: {non_terminal} -> {production}")
                
                if production == 'ε':
                    print(f"    Eliminando producción ε")
                    continue
                
                new_prods = self.generate_new_productions(production, nullable_symbols)
                
                for new_prod in new_prods:
                    new_productions_for_nt.add(new_prod)
                    print(f"    Nueva producción: {non_terminal} -> {new_prod}")
            
            # Agregar producciones únicas
            new_grammar[non_terminal] = list(new_productions_for_nt)
        
        # Paso 3: Manejar el símbolo inicial si es anulable
        if self.start_symbol in nullable_symbols:
            print(f"\n⚠️  El símbolo inicial {self.start_symbol} es anulable.")
            print(f"   Se debe agregar una nueva producción para generar la cadena vacía si es necesario.")
        
        # Actualizar la gramática
        self.productions = new_grammar
        
        print("\n=== GRAMÁTICA SIN PRODUCCIONES EPSILON ===")
        self.display_final_grammar()
    
    def display_final_grammar(self):
        """Muestra la gramática final sin producciones ε."""
        print("\nProducciones finales:")
        for non_terminal in sorted(self.non_terminals):
            if non_terminal in self.productions and self.productions[non_terminal]:
                productions_str = ' | '.join(sorted(self.productions[non_terminal]))
                print(f"  {non_terminal} -> {productions_str}")
            elif non_terminal in self.productions:
                print(f"  {non_terminal} -> (sin producciones válidas)")


def main():
    """Función principal del programa."""
    print("SIMPLIFICADOR DE GRAMÁTICAS - ELIMINACIÓN DE PRODUCCIONES EPSILON")
    print("="*70)
    
    grammar_files = ['grammar1.txt', 'grammar2.txt', 'grammar3.txt']
    
    for filename in grammar_files:
        print(f"\n{'='*20} PROCESANDO {filename} {'='*20}")
        
        simplifier = GrammarSimplifier()
        
        # Cargar y parsear la gramática
        if not simplifier.parse_grammar_file(filename):
            print(f"❌ Error al procesar {filename}")
            continue
        
        # Mostrar gramática original
        simplifier.display_grammar()
        
        # Eliminar producciones ε
        simplifier.remove_epsilon_productions()
        
        print(f"\n✅ Procesamiento de {filename} completado")


if __name__ == "__main__":
    main()