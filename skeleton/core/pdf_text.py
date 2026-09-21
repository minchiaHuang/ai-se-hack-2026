"""Small, bounded PDF text-layer reader for the offline resume upload.

It deliberately understands only ordinary PDF text streams. CID fonts, OCR and
encrypted files must be refused rather than turned into evidence with invented
resume-line citations.
"""
import re
import zlib


MAX_PAGES = 20
MAX_STREAMS = 200
MAX_DECOMPRESSED_STREAM = 512 * 1024
MAX_TEXT_CHARS = 200 * 1024


class PdfTextError(ValueError):
    """A PDF cannot safely provide numbered resume evidence."""


class PdfString(str):
    """A string operand, kept distinct from a PDF operator with the same text."""


def extract_lines(data):
    """Return visible text lines from a small, unencrypted PDF text layer."""
    if not data.startswith(b"%PDF-"):
        raise PdfTextError("This file is not a PDF, so it was not read.")
    if re.search(rb"/Encrypt\b", data):
        raise PdfTextError("This PDF is encrypted, so it cannot be read here. Paste its text instead.")
    pages = len(re.findall(rb"/Type\s*/Page\b", data))
    if pages > MAX_PAGES:
        raise PdfTextError(f"This PDF has more than {MAX_PAGES} pages, so it was not read.")

    lines = []
    for dictionary, stream in _streams(data):
        content = _content(dictionary, stream)
        if content is not None:
            lines.extend(_text_lines(content))
        if sum(len(line) for line in lines) > MAX_TEXT_CHARS:
            raise PdfTextError("This PDF has too much text to read safely.")

    cleaned = [_clean(line) for line in lines]
    cleaned = [line for line in cleaned if line]
    if not cleaned or not _readable(cleaned):
        raise PdfTextError(
            "This PDF looks like a scan or a photo, so there is no readable text in it. "
            "Paste the text instead, or upload a .txt file."
        )
    return cleaned


def _streams(data):
    """Yield bounded PDF streams. A malformed stream is ignored, not retried."""
    pattern = re.compile(rb"(<<.*?>>)\s*stream[ \t]*\r?\n(.*?)\r?\nendstream", re.DOTALL)
    for count, match in enumerate(pattern.finditer(data)):
        if count == MAX_STREAMS:
            break
        yield match.group(1), match.group(2)


def _content(dictionary, stream):
    if b"/FlateDecode" not in dictionary:
        return stream if b"/Filter" not in dictionary else None
    try:
        inflater = zlib.decompressobj()
        content = inflater.decompress(stream, MAX_DECOMPRESSED_STREAM + 1)
        if len(content) > MAX_DECOMPRESSED_STREAM or inflater.unconsumed_tail:
            return None
        content += inflater.flush(MAX_DECOMPRESSED_STREAM + 1 - len(content))
        return content if len(content) <= MAX_DECOMPRESSED_STREAM else None
    except zlib.error:
        return None


def _text_lines(content):
    lines, current, operands = [], [], []
    in_text = False
    matrix_y = None

    def flush():
        if current:
            lines.append("".join(current))
            current.clear()

    for token in _tokens(content):
        operator = token if type(token) is str else None
        if operator == "BT":
            in_text, operands = True, []
            matrix_y = None
            continue
        if operator == "ET":
            flush()
            in_text, operands = False, []
            matrix_y = None
            continue
        if not in_text:
            continue
        if operator == "T*":
            flush()
        elif operator in ("Td", "TD"):
            delta_y = _number(operands[-1] if operands else None)
            if delta_y not in (None, 0):
                flush()
                matrix_y = (matrix_y or 0) + delta_y
            operands.clear()
        elif operator == "Tm":
            new_y = _number(operands[-1] if len(operands) >= 6 else None)
            if current and new_y is not None and matrix_y is not None and new_y != matrix_y:
                flush()
            if new_y is not None:
                matrix_y = new_y
            operands.clear()
        elif operator == "Tj":
            _append(current, _last_text(operands))
            operands.clear()
        elif operator == "TJ":
            value = operands.pop() if operands else []
            if isinstance(value, list):
                _append(current, "".join(item for item in value
                                         if isinstance(item, str) and not _is_number(item)))
            operands.clear()
        elif operator in ("'", '"'):
            flush()
            _append(current, _last_text(operands))
            operands.clear()
        elif isinstance(token, str) and token not in ("[", "]"):
            operands.append(token)
        elif isinstance(token, list):
            operands.append(token)
    return lines


def _append(current, text):
    if text:
        current.append(text)


def _last_text(operands):
    for index in range(len(operands) - 1, -1, -1):
        if isinstance(operands[index], PdfString):
            return operands.pop(index)
    return ""


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_number(value):
    return _number(value) is not None


def _tokens(content):
    """Tokenise the small PostScript subset used by PDF text operators."""
    tokens, array, index = [], None, 0
    while index < len(content):
        byte = content[index]
        if byte in b" \t\r\n\f\0":
            index += 1
            continue
        if byte == ord("%"):
            end = content.find(b"\n", index)
            index = len(content) if end < 0 else end + 1
            continue
        if byte == ord("("):
            value, index = _literal(content, index + 1)
        elif byte == ord("<") and not content[index:index + 2] == b"<<":
            end = content.find(b">", index + 1)
            if end < 0:
                break
            raw = re.sub(rb"\s", b"", content[index + 1:end])
            try:
                value = PdfString(_decode(bytes.fromhex(raw.decode("ascii"))))
            except (ValueError, UnicodeDecodeError):
                value = ""
            index = end + 1
        elif byte == ord("["):
            array, index = [], index + 1
            continue
        elif byte == ord("]"):
            value, array, index = array or [], None, index + 1
        else:
            end = index
            while end < len(content) and content[end] not in b" \t\r\n\f\0()<>[]/%":
                end += 1
            if end == index:
                index += 1
                continue
            value = content[index:end].decode("latin-1")
            index = end
        if array is not None:
            array.append(value)
        else:
            tokens.append(value)
    return tokens


def _literal(data, index):
    output, depth = bytearray(), 1
    while index < len(data) and depth:
        byte = data[index]
        if byte == ord("\\"):
            index += 1
            if index >= len(data):
                break
            escaped = data[index]
            mapped = {ord("n"): b"\n", ord("r"): b"\r", ord("t"): b"\t",
                      ord("b"): b"\b", ord("f"): b"\f"}
            if escaped in mapped:
                output.extend(mapped[escaped])
                index += 1
            elif escaped in b"01234567":
                digits = bytes([escaped])
                for _ in range(2):
                    if index + 1 < len(data) and data[index + 1] in b"01234567":
                        index += 1
                        digits += bytes([data[index]])
                output.append(int(digits, 8))
                index += 1
            else:
                output.append(escaped)
                index += 1
        elif byte == ord("("):
            depth += 1
            output.append(byte)
            index += 1
        elif byte == ord(")"):
            depth -= 1
            index += 1
            if depth:
                output.append(byte)
        else:
            output.append(byte)
            index += 1
    return PdfString(_decode(bytes(output))), index


def _decode(raw):
    if raw.startswith(b"\xfe\xff"):
        return raw[2:].decode("utf-16-be", errors="replace")
    if raw.startswith(b"\xff\xfe"):
        return raw[2:].decode("utf-16-le", errors="replace")
    return raw.decode("latin-1", errors="replace")


def _clean(text):
    return re.sub(r"\s+", " ", text).strip()


def _readable(lines):
    text = "".join(lines)
    printable = sum(char.isprintable() and char != "\ufffd" for char in text)
    return bool(text) and printable / len(text) >= 0.9
