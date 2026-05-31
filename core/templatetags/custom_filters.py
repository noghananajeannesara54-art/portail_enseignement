from django import template

register = template.Library()

@register.filter
def fix_encoding(text):
    """Corrige les problèmes d'encodage des caractères spéciaux"""
    if not text:
        return text
    
    # Remplacer les apostrophes mal encodées
    replacements = {
        '': "'",
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '"': '"',
        '–': '-',
        '—': '--',
        '…': '...',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
