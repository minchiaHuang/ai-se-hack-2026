"""Generate the tiny PDFs used by test_pdf_text.py; do not hand-edit binaries."""
from pathlib import Path
import zlib


HERE = Path(__file__).parent


def pdf(objects):
    body = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, object_body in enumerate(objects, 1):
        offsets.append(len(body))
        body.extend(f"{number} 0 obj\n".encode())
        body.extend(object_body)
        body.extend(b"\nendobj\n")
    xref = len(body)
    body.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    body.extend(b"".join(f"{offset:010} 00000 n \n".encode() for offset in offsets[1:]))
    body.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(body)


def stream(content):
    compressed = zlib.compress(content)
    return (f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n".encode()
            + compressed + b"\nendstream")


def page(content):
    return pdf([
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        stream(content),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ])


def main():
    (HERE / "resume_text.pdf").write_bytes(page(
        b"BT\n/F1 12 Tf\n1 0 0 1 72 720 Tm\n(Leah Example) Tj\n"
        b"1 0 0 1 72 702 Tm\n(Commercial cook) Tj\nT*\n(Food safety and kitchen work) Tj\nET\n"))
    (HERE / "resume_hex.pdf").write_bytes(page(
        b"BT\n/F1 12 Tf\n72 720 Td\n<4A6F7320526573756D65> Tj\n0 -18 Td\n"
        b"[(Cooked ) -120 (meals)] TJ\n(Food safety) '\nET\n"))
    # What Quartz writes (Pages, Word for Mac, Preview): one tiny string per
    # glyph, the kerning between them, and a word gap carried by the gap alone.
    (HERE / "resume_kerned.pdf").write_bytes(page(
        b"BT\n/F1 11 Tf\n11 0 0 11 72 720 Tm\n"
        b"[ (2) -0.2 (0) -0.2 (1) -0.2 (6) -0.2 (-2) -0.2 (0) -0.2 (2) -0.2 (2) -0.2 ( )"
        b" 0.2 (H) -0.2 (e) -0.2 (a) -0.2 (d) -0.2 ( ) 0.2 (co) -0.2 (o) -0.2 (k) ] TJ\n"
        b"11 0 0 11 72 704 Tm\n[ (Cooked) -300 (for) -300 (150) -300 (guests) ] TJ\nET\n"))
    (HERE / "cid_font.pdf").write_bytes(page(
        b"BT\n/F2 12 Tf\n72 720 Td\n<00240050004C0051004400032B0044> Tj\nET\n"))
    (HERE / "scanned.pdf").write_bytes(page(b"q\n100 0 0 100 0 0 cm\n/Im0 Do\nQ\n"))
    (HERE / "malformed.pdf").write_bytes(b"%PDF-1.4\n<< /Filter /FlateDecode >>\nstream\nnot-zlib\nendstream\n")
    (HERE / "encrypted.pdf").write_bytes(b"%PDF-1.4\n<< /Encrypt 4 0 R >>\n%%EOF\n")


if __name__ == "__main__":
    main()
