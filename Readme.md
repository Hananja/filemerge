# Filemerge

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ein leistungsstarker Seriendokumentgenerator, der Jinja2-Templates mit CSV-Daten kombiniert, um automatisch mehrere Dokumente zu erstellen.

## 🚀 Features

- **Flexible Templates**: Nutzen Sie die volle Power von Jinja2-Templates
- **CSV-Integration**: Einfache Verarbeitung von CSV-Dateien als Datenquelle
- **Batch-Generierung**: Erstellen Sie hunderte Dokumente mit einem Befehl
- **Anpassbare Header**: Überschreiben Sie CSV-Spaltenüberschriften nach Bedarf
- **Selektive Verarbeitung**: Wählen Sie spezifische Zeilen oder Bereiche aus
- **UTF-8 Unterstützung**: Vollständige Unicode-Unterstützung für internationale Zeichen

## 📦 Installation

### Mit pipx (empfohlen)
```bash
pipx install filemerge
```

### Mit pip
```bash
pip install filemerge
```

### Aus dem Repository
```bash
pipx install git+https://github.com/Hananja/filemerge.git
```

## 🛠️ Verwendung

### Grundlegende Syntax
```bash
filemerge <template_datei> <csv_datei> <ausgabe_ordner>
```

### Beispiele

#### Einfaches Beispiel
```bash
filemerge brief_template.txt kontakte.csv output/
```

#### Mit benutzerdefinierten Headern
```bash
filemerge template.html daten.csv briefe/ --headers Name,Email,Firma,Adresse
```

#### Spezifische Zeilen auswählen
```bash
# Nur Zeilen 1, 3, 4, 5 und 7 verarbeiten
filemerge template.txt data.csv output/ --select 1,3-5,7
```

#### CSV ohne Header, automatische Spaltennamen (col_1, col_2, ...)
filemerge template.txt daten.csv output/ --no-headers

#### CSV ohne Header, aber mit eigenen Spaltennamen
filemerge template.txt daten.csv output/ --no-headers --headers Name,Email,Telefon

#### Kombination mit Zeilenauswahl
filemerge template.txt daten.csv output/ --no-headers --select 1-5

#### Dateinamen aus Name-Spalte generieren
filemerge template.txt kontakte.csv output/ -t "{{ Name }}.txt"

#### Kombiniert mehrere Felder
filemerge template.txt daten.csv output/ -t "{{ Firma }}_{{ Name }}_{{ Datum }}.html"

#### Mit Unterordnern (falls Betriebssystem unterstützt)
filemerge template.txt daten.csv output/ -t "{{ Kategorie }}/{{ Name }}.txt"

#### Fallback auf Standard wenn Template-Fehler auftreten
filemerge template.txt daten.csv output/ -t "{{ UngueltigesSpalte }}.txt"

### Template-Beispiel

**brief_template.txt:**
```jinja2
Sehr geehrte(r) {{ Name }},

vielen Dank für Ihr Interesse an unseren Produkten. 

Ihre Kontaktdaten:
- Email: {{ Email }}
- Firma: {{ Firma }}
- Telefon: {{ Telefon }}

Mit freundlichen Grüßen,
Ihr Team
```

**kontakte.csv:**
```csv
Name,Email,Firma,Telefon
Max Mustermann,max@example.com,Beispiel GmbH,+49123456789
Anna Schmidt,anna@test.de,Test AG,+49987654321
```

**Generierte Ausgabe:**
- `output_1.txt`: Brief für Max Mustermann
- `output_2.txt`: Brief für Anna Schmidt

## 📋 Kommandozeilen-Optionen

| Option | Beschreibung | Beispiel |
|--------|--------------|----------|
| `--headers` | Überschreibt CSV-Spaltenüberschriften | `--headers Name,Email,Firma` |
| `--select` | Wählt spezifische Zeilen aus (1-basiert) | `--select 1,3-5,7` |
| `--help` | Zeigt Hilfe an | `--help` |

### Zeilen-Auswahl im Detail

Die `--select` Option unterstützt:
- **Einzelne Zeilen**: `1,3,5` (Zeilen 1, 3 und 5)
- **Bereiche**: `2-5` (Zeilen 2 bis 5)
- **Kombinationen**: `1,3-5,8,10-12` (Zeile 1, Zeilen 3-5, Zeile 8, Zeilen 10-12)

## 🎯 Anwendungsfälle

- Serienbriefe mit LaTeX oder anderen textbasierten Systemen
### 📧