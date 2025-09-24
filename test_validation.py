from grammar_simplifier import GrammarSimplifier

def test_validation():
    """Prueba la validación de formato de producciones."""
    simplifier = GrammarSimplifier()
    
    print("=== PRUEBA DE VALIDACIÓN ===")
    
    # Casos válidos
    valid_cases = [
        "S -> aAa | bBb | ε",
        "A -> C | a",
        "B -> CDE",
        "C -> ε"
    ]
    
    # Casos inválidos
    invalid_cases = [
        "s -> aAa",  # No-terminal debe ser mayúscula
        "S > aAa",   # Flecha incorrecta
        "S -> aAa |",  # Termina con |
        "S ->",      # Sin producción
        "",          # Línea vacía
        "S -> aAa | | bBb"  # Doble |
    ]
    
    print("\nCasos válidos:")
    for case in valid_cases:
        result = simplifier.validate_production_line(case)
        print(f"  '{case}' -> {'✓' if result else '❌'}")
    
    print("\nCasos inválidos:")
    for case in invalid_cases:
        result = simplifier.validate_production_line(case)
        print(f"  '{case}' -> {'❌' if not result else '✓ (ERROR: debería ser inválido)'}")
    
    print("\nProbando archivo con formato inválido:")
    success = simplifier.parse_grammar_file('invalid_grammar.txt')
    print(f"Resultado: {'✓ Parseado' if success else '❌ Error detectado (correcto)'}")

if __name__ == "__main__":
    test_validation()