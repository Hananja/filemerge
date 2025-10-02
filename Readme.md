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
```bash
filemerge template.txt daten.csv output/ --no-headers
```

#### CSV ohne Header, aber mit eigenen Spaltennamen
```bash
filemerge template.txt daten.csv output/ --no-headers --headers Name,Email,Telefon
```

#### Kombination mit Zeilenauswahl
```bash
filemerge template.txt daten.csv output/ --no-headers --select 1-5
```

#### Dateinamen aus Name-Spalte generieren
```bash
filemerge template.txt kontakte.csv output/ -t "{{ Name }}.txt"
```

#### Kombiniert mehrere Felder
```bash
filemerge template.txt daten.csv output/ -t "{{ Firma }}_{{ Name }}_{{ Datum }}.html"
```

#### Mit Unterordnern (falls Betriebssystem unterstützt)
```bash
filemerge template.txt daten.csv output/ -t "{{ Kategorie }}/{{ Name }}.txt"
```

#### Fallback auf Standard wenn Template-Fehler auftreten
```bash
filemerge template.txt daten.csv output/ -t "{{ UngueltigesSpalte }}.txt"
```
#### Standard CSV mit Komma
```bash
filemerge template.txt data.csv output/
```

#### Semikolon-getrennte Datei (häufig in Europa)
```bash
filemerge template.txt data.csv output/ -d ";"
```

#### Tab-getrennte Datei (TSV)
```bash
filemerge template.txt data.tsv output/ --delimiter "\\t"
```

#### Pipe-getrennte Datei
```bash
filemerge template.txt data.txt output/ -d "|"
```

#### Kombination mit anderen Optionen
```bash
filemerge template.txt data.csv output/ -d ";" -t "{{ Name }}.html" --no-headers
```

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

```
usage: filemerge [-h] [--headers HEADERS] [--select SELECT] [-n] [-t FILE_TEMPLATE] [-d DELIMITER]
                 template csvfile output_dir

Seriendokumentgenerator: Erstelle Dokumente aus Jinja-Templates und CSV-Daten.

positional arguments:
  template              Pfad zur Jinja-Template-Datei
  csvfile               Pfad zur CSV-Datei
  output_dir            Ausgabeordner für generierte Dateien

options:
  -h, --help            show this help message and exit
  --headers HEADERS     Überschreibe CSV-Spaltenüberschriften; kommasepariert z.B.
                        Name,Adresse,Telefon
  --select SELECT       Auswahl einzelner oder mehrerer Zeilen und Bereiche 1,3-5,7 (1-basierte
                        Indizes)
  -n, --no-headers      CSV enthält keine Spaltenüberschriften; Daten beginnen ab der ersten Zeile
  -t, --file-template FILE_TEMPLATE
                        Jinja-Template für Dateinamen, z.B. "{{ Name }}_{{ Datum }}.txt"
  -d, --delimiter DELIMITER
                        CSV-Trennzeichen (Standard: Komma). Für Tab verwenden Sie "\t"

```

### Zeilen-Auswahl im Detail

Die `--select` Option unterstützt:
- **Einzelne Zeilen**: `1,3,5` (Zeilen 1, 3 und 5)
- **Bereiche**: `2-5` (Zeilen 2 bis 5)
- **Kombinationen**: `1,3-5,8,10-12` (Zeile 1, Zeilen 3-5, Zeile 8, Zeilen 10-12)

## 🎯 Anwendungsfälle

- Serienbriefe mit LaTeX oder anderen textbasierten Systemen