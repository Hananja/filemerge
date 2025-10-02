import argparse
import csv
from jinja2 import Environment, FileSystemLoader
import os

def read_csv(file_path, override_headers=None, select_rows=None):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        if not reader:
            raise ValueError("CSV Datei ist leer")
        if override_headers:
            headers = override_headers
        else:
            headers = reader[0]
            reader = reader[1:]

        if select_rows:
            selected = [reader[i] for i in select_rows if i < len(reader)]
        else:
            selected = reader

        data = [{headers[j]: row[j] if j < len(row) else '' for j in range(len(headers))} for row in selected]
    return data

def render_templates(template_path, csv_path, output_dir, override_headers=None, select_rows=None):
    template_dir = os.path.dirname(template_path) or '.'
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    data = read_csv(csv_path, override_headers=override_headers, select_rows=select_rows)

    os.makedirs(output_dir, exist_ok=True)

    for i, context in enumerate(data, 1):
        output_content = template.render(context)
        output_file = os.path.join(output_dir, f"output_{i}.txt")
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

    args = parser.parse_args()

    render_templates(args.template, args.csvfile, args.output_dir, override_headers=args.headers, select_rows=args.select)

if __name__ == '__main__':
    main()

