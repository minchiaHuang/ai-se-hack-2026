"""The resume PDF reader is deliberately small and fails closed."""
from pathlib import Path
import unittest

from skeleton.core.pdf_text import PdfTextError, extract_lines


FIXTURES = Path(__file__).parent / "fixtures"


class PdfText(unittest.TestCase):
    def read(self, name):
        return extract_lines((FIXTURES / name).read_bytes())

    def test_text_positions_make_resume_lines(self):
        self.assertEqual(self.read("resume_text.pdf"), [
            "Leah Example", "Commercial cook", "Food safety and kitchen work"
        ])

    def test_hex_strings_tj_arrays_and_quote_operator_are_text(self):
        self.assertEqual(self.read("resume_hex.pdf"), [
            "Jos Resume", "Cooked meals", "Food safety"
        ])

    def test_years_and_numbers_survive_a_kerned_tj_array(self):
        """Quartz splits a line into one string per glyph, and a resume's dates
        and quantities read as numbers. Dropping them would delete the evidence."""
        self.assertEqual(self.read("resume_kerned.pdf"),
                         ["2016-2022 Head cook", "Cooked for 150 guests"])

    def test_a_font_this_reader_cannot_decode_is_not_called_a_scan(self):
        """Chrome and Google Docs write CID fonts. Refusing is right; telling the
        person their text PDF is a photo is a wrong reason, and reasons matter here."""
        with self.assertRaisesRegex(PdfTextError, "cannot decode"):
            self.read("cid_font.pdf")

    def test_scanned_and_malformed_files_are_not_evidence(self):
        for name in ("scanned.pdf", "malformed.pdf"):
            with self.subTest(name=name), self.assertRaisesRegex(PdfTextError, "scan or a photo"):
                self.read(name)

    def test_encrypted_file_is_refused_without_attempting_text(self):
        with self.assertRaisesRegex(PdfTextError, "encrypted"):
            self.read("encrypted.pdf")


if __name__ == "__main__":
    unittest.main()
