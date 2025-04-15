import unicodedata

def normalize_name(name):
    """Normaliza nombres quitando tildes y espacios extras."""
    if not isinstance(name, str):
        return None
    name = unicodedata.normalize("NFKD", name.strip()).encode("ASCII", "ignore").decode("utf-8")
    return name
