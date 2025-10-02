"""
Filemerge - Ein leistungsstarker Seriendokumentgenerator

Kombiniert Jinja2-Templates mit CSV-Daten um automatisch mehrere Dokumente zu erstellen.
"""

from .filemerge import main, render_templates, read_csv

__version__ = "0.1.0"
__all__ = ["main", "render_templates", "read_csv"]