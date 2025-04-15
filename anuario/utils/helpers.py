def safe_divide(a, b):
    """Evita dividir por cero."""
    return a / b if b != 0 else None

def promedio_valores(valores):
    """Calcula promedio ignorando None y NaNs."""
    limpios = [v for v in valores if v is not None and not pd.isna(v)]
    return sum(limpios) / len(limpios) if limpios else None
