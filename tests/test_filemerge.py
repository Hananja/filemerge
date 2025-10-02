import unittest
import tempfile
import os
import subprocess
import sys
from unittest import mock

import filemerge.main


class TestFilemergeIntegration(unittest.TestCase):

    def setUp(self):
        # Temporären Ordner für Testdateien und Ausgabe erstellen
        self.test_dir = tempfile.TemporaryDirectory()
        self.output_dir = os.path.join(self.test_dir.name, "output")
        os.mkdir(self.output_dir)
        print("Test directory: {}".format(self.test_dir))

        # Beispiel-Jinja2-Template mit Platzhaltern
        self.template_path = os.path.join(self.test_dir.name, "template.txt")
        with open(self.template_path, "w", encoding="utf-8") as f:
            f.write("Name: {{ Name }}\nAlter: {{ Alter }}\nStadt: {{ Stadt }}\n\n")

        # Beispiel-CSV-Datei
        self.csv_path = os.path.join(self.test_dir.name, "data.csv")
        with open(self.csv_path, "w", encoding="utf-8", newline='') as f:
            f.write("Name,Alter,Stadt\nAlice,30,Berlin\nBob,25,Hamburg\nCharlie,35,München\n")

    def tearDown(self):
        self.test_dir.cleanup()
        pass

    def test_cli_generate_documents(self):
        # Kommandozeilenaufruf des Scripts (seriendokument.py muss im selben Ordner liegen)
        test_args = [
            "main.py",     # Skriptname
            self.template_path,
            self.csv_path,
            self.output_dir,
            #"--select", "1,3"
            "--file-template=output-{{ Name }}.txt"
        ]

        # Skript ausführen
        # result = subprocess.run(cmd, capture_output=True, text=True)
        # self.assertEqual(0, result.returncode, msg=f"Fehler: {result.stderr}")

        # Mock argv
        with mock.patch.object(sys, 'argv', test_args):
            # main() führt den kompletten Ablauf durch, inkl. Argumenten parsen und Dokumente generieren
            filemerge.main.cli()

        # Prüfen, ob Ausgabe erzeugt wurde
        output_files = sorted(f for f in os.listdir(self.output_dir) if f.endswith(".txt"))
        self.assertEqual(2, len(output_files) )

        # Inhalt der erzeugten Datei prüfen
        with open(os.path.join(self.output_dir, output_files[0]), encoding="utf-8") as f:
            content1 = f.read()
        with open(os.path.join(self.output_dir, output_files[1]), encoding="utf-8") as f:
            content2 = f.read()

        self.assertIn("Name: Alice", content1)
        self.assertIn("Stadt: Berlin", content1)
        self.assertIn("Name: Charlie", content2)
        self.assertIn("Stadt: München", content2)

if __name__ == "__main__":
    unittest.main()
