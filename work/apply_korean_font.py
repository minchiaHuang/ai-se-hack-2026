from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from lxml import etree
import os

DOCX = Path('AI_for_Social_Enterprise_Hackathon_Research_Brief_v1.4_Korean.docx')
TEMP = DOCX.with_suffix('.korean-font.docx')
FONT = 'AppleGothic'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}


def tag(name):
    return f'{{{W}}}{name}'


def set_font(fonts):
    for attr in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
        fonts.set(tag(attr), FONT)


def replace_empty_page_break_paragraphs(root):
    """Avoid a lone page-break glyph being rendered as a square."""
    body = root.find('w:body', NS)
    if body is None:
        return
    paragraphs = list(body.findall('w:p', NS))
    for index, paragraph in enumerate(paragraphs[:-1]):
        has_only_page_break = (
            not paragraph.xpath('.//w:t', namespaces=NS)
            and len(paragraph.xpath('.//w:br[@w:type="page"]', namespaces=NS)) == 1
            and len(paragraph.xpath('.//w:br', namespaces=NS)) == 1
        )
        if not has_only_page_break:
            continue
        following = paragraphs[index + 1]
        ppr = following.find('w:pPr', NS)
        if ppr is None:
            ppr = etree.Element(tag('pPr'))
            following.insert(0, ppr)
        if ppr.find('w:pageBreakBefore', NS) is None:
            ppr.append(etree.Element(tag('pageBreakBefore')))
        body.remove(paragraph)


with ZipFile(DOCX) as source, ZipFile(TEMP, 'w', ZIP_DEFLATED) as target:
    for item in source.infolist():
        data = source.read(item.filename)
        if not (item.filename.startswith('word/') and item.filename.endswith('.xml')) or item.filename == 'word/numbering.xml':
            target.writestr(item, data)
            continue
        root = etree.fromstring(data)
        if item.filename == 'word/document.xml':
            replace_empty_page_break_paragraphs(root)
        for fonts in root.xpath('.//w:rFonts', namespaces=NS):
            set_font(fonts)
        for run in root.xpath('.//w:r[w:t]', namespaces=NS):
            rpr = run.find('w:rPr', NS)
            if rpr is None:
                rpr = etree.Element(tag('rPr'))
                run.insert(0, rpr)
            fonts = rpr.find('w:rFonts', NS)
            if fonts is None:
                fonts = etree.Element(tag('rFonts'))
                rpr.insert(0, fonts)
            set_font(fonts)
        if item.filename == 'word/fontTable.xml' and not root.xpath(".//w:font[@w:name='Apple SD Gothic Neo']", namespaces=NS):
            font = etree.SubElement(root, tag('font'))
            font.set(tag('name'), FONT)
        target.writestr(item, etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True))

os.replace(TEMP, DOCX)
print(f'Applied {FONT} to all non-numbering text runs and styles.')
