import argparse
import csv
from jinja2 import Environment, FileSystemLoader, Template
import os
import re

def read_csv(file_path, override_headers=None, select_rows=None, no_headers=False, delimiter=','):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=delimiter))
        if not reader:
            raise ValueError("CSV Datei ist leer")

        if override_headers:
            headers = override_headers
            # Bei override_headers verwenden wir alle Zeilen als Daten
            if no_headers:
                # Alle Zeilen sind Daten
                data_rows = reader
            else:
                # Erste Zeile überspringen (normalerweise Header)
                data_rows = reader[1:]
        elif no_headers:
            # Keine Header erwartet - generiere automatische Header (col_1, col_2, ...)
            if not reader:
                headers = []
                data_rows = []
            else:
                headers = [f"col_{i+1}" for i in range(len(reader[0]))]
                data_rows = reader  # Alle Zeilen sind Daten
        else:
            # Standard: Erste Zeile als Header verwenden
            headers = reader[0]
            data_rows = reader[1:]

        if select_rows:
            selected = [data_rows[i] for i in select_rows if i < len(data_rows)]
        else:
            selected = data_rows

        data = [{headers[j]: row[j] if j < len(row) else '' for j in range(len(headers))} for row in selected]
    return data

def sanitize_filename(filename):
    """Bereinigt einen Dateinamen von ungültigen Zeichen für das Dateisystem"""
    # Entferne oder ersetze ungültige Zeichen für Windows/Unix Dateisysteme
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Entferne führende/nachfolgende Leerzeichen und Punkte
    filename = filename.strip('. ')
    # Verhindere leeren Dateinamen
    if not filename:
        filename = 'unnamed'
    return filename

def render_templates(template_path, csv_path, output_dir, override_headers=None, select_rows=None, no_headers=False, file_template=None, delimiter=','):
    template_dir = os.path.dirname(template_path) or '.'
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    # Template für Dateinamen erstellen, falls angegeben
    filename_template = None
    if file_template:
        filename_template = Template(file_template)

    data = read_csv(csv_path, override_headers=override_headers, select_rows=select_rows, no_headers=no_headers, delimiter=delimiter)

    os.makedirs(output_dir, exist_ok=True)

    for i, context in enumerate(data, 1):
        output_content = template.render(context)

        # Dateinamen generieren
        if filename_template:
            try:
                filename = filename_template.render(context)
                filename = sanitize_filename(filename)
                # Falls der gerenderte Dateiname leer ist, Fallback verwenden
                if not filename:
                    filename = f"output_{i}.txt"
                # Dateiendung hinzufügen, falls nicht vorhanden
                elif '.' not in filename:
                    filename += '.txt'
            except Exception as e:
                print(f"Warnung: Fehler beim Generieren des Dateinamens für Zeile {i}: {e}")
                filename = f"output_{i}.txt"
        else:
            filename = f"output_{i}.txt"

        output_file = os.path.join(output_dir, filename)

        # Prüfe auf Dateinamenskonflikte und füge Suffix hinzu falls nötig
        counter = 1
        original_output_file = output_file
        while os.path.exists(output_file):
            name, ext = os.path.splitext(original_output_file)
            output_file = f"{name}_{counter}{ext}"
            counter += 1

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Datei erstellt: {output_file}")

def parse_headers(arg):
    # Kommaseparierte Header, z.B. Name,Adresse,Telefon
    return [h.strip() for h in arg.split(',') if h.strip()]

def parse_select_rows(arg):
    # Erlaubt einzelne Zahlen und Bereiche mit Bindestrich, z.B. 1,3-5,7
    result = []
    parts = arg.split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-', 1)
            try:
                start_i = int(start)-1
                end_i = int(end)-1
                if start_i <= end_i:
                    result.extend(range(start_i, end_i+1))
                else:
                    result.extend(range(end_i, start_i+1))
            except ValueError:
                raise argparse.ArgumentTypeError(f"Ungültiger Bereich: {part}")
        else:
            try:
                result.append(int(part)-1)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Ungültige Zahl: {part}")
    return sorted(set(result))

def main():
    parser = argparse.ArgumentParser(
        description="Seriendokumentgenerator: Erstelle Dokumente aus Jinja-Templates und CSV-Daten.")
    parser.add_argument('template', help='Pfad zur Jinja-Template-Datei')
    parser.add_argument('csvfile', help='Pfad zur CSV-Datei')
    parser.add_argument('output_dir', help='Ausgabeordner für generierte Dateien')
    parser.add_argument('--headers', type=parse_headers, help='Überschreibe CSV-Spaltenüberschriften; kommasepariert z.B. Name,Adresse,Telefon')
    parser.add_argument('--select', type=parse_select_rows, help='Auswahl einzelner oder mehrerer Zeilen und Bereiche 1,3-5,7 (1-basierte Indizes)')
    parser.add_argument('-n', '--no-headers', action='store_true', help='CSV enthält keine Spaltenüberschriften; Daten beginnen ab der ersten Zeile')
    parser.add_argument('-t', '--file-template', help='Jinja-Template für Dateinamen, z.B. "{{ Name }}_{{ Datum }}.txt"')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV-Trennzeichen (Standard: Komma). Für Tab verwenden Sie "\\t"')

    args = parser.parse_args()

    # Erlaube spezielle Zeichen-Notationen
    delimiter = args.delimiter
    if delimiter == '\\t':
        delimiter = '\t'
    elif delimiter == '\\n':
        delimiter = '\n'
    elif delimiter == '\\r':
        delimiter = '\r'

    render_templates(args.template, args.csvfile, args.output_dir,
                     override_headers=args.headers, select_rows=args.select,
                     no_headers=args.no_headers, file_template=args.file_template,
                     delimiter=delimiter)

if __name__ == '__main__':
    main()