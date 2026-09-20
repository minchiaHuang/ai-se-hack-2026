from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}


def main(source_path: str, translations_path: str, output_path: str) -> None:
    translations = {item['source']: item['target'] for item in json.loads(Path(translations_path).read_text())}
    source = Path(source_path)
    output = Path(output_path)
    changed = 0

    with ZipFile(source) as in_zip, ZipFile(output, 'w', ZIP_DEFLATED) as out_zip:
        for item in in_zip.infolist():
            data = in_zip.read(item.filename)
            if not (item.filename.startswith('word/') and item.filename.endswith('.xml')):
                out_zip.writestr(item, data)
                continue
            root = etree.fromstring(data)
            for text_node in root.xpath('.//w:t', namespaces=NS):
                value = text_node.text or ''
                if re.search(r'[\u3400-\u9fff]', value):
                    replacement = translations.get(value)
                    if replacement is None:
                        raise RuntimeError(f'Missing translation for: {value!r}')
                    text_node.text = replacement
                    if replacement.startswith(' ') or replacement.endswith(' '):
                        text_node.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                    changed += 1
            out_zip.writestr(item, etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True))

    print(f'Replaced {changed} Chinese OOXML text nodes with Korean translations.')


if __name__ == '__main__':
    main(*sys.argv[1:])
