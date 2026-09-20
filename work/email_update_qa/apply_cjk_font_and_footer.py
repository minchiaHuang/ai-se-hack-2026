from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
FONT = "Arial Unicode MS"
FILES = [
    "AI_for_Social_Enterprise_Hackathon_Research_Brief_v1.2.docx",
    "AI_for_Social_Enterprise_Hackathon_Research_Brief_v1.4_Simplified_Chinese.docx",
    "AI_for_Social_Enterprise_Hackathon_Research_Brief_v1.4_Korean.docx",
]


def tag(name):
    return f"{{{W}}}{name}"


for path_str in FILES:
    path = Path(path_str)
    temp = path.with_suffix(".fontfix.docx")
    with ZipFile(path) as source, ZipFile(temp, "w", ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if not (item.filename.startswith("word/") and item.filename.endswith(".xml")):
                target.writestr(item, data)
                continue
            root = etree.fromstring(data)
            for fonts in root.xpath(".//w:rFonts", namespaces=NS):
                fonts.set(tag("eastAsia"), FONT)
            for run in root.xpath(".//w:r[w:t]", namespaces=NS):
                rpr = run.find("w:rPr", NS)
                if rpr is None:
                    rpr = etree.Element(tag("rPr"))
                    run.insert(0, rpr)
                fonts = rpr.find("w:rFonts", NS)
                if fonts is None:
                    fonts = etree.Element(tag("rFonts"))
                    rpr.insert(0, fonts)
                fonts.set(tag("eastAsia"), FONT)
            for run in root.xpath(".//w:tc//w:r[w:t]", namespaces=NS):
                text = "".join(run.xpath(".//w:t/text()", namespaces=NS))
                if not any("\u3400" <= char <= "\u9fff" or "\uac00" <= char <= "\ud7a3" for char in text):
                    continue
                rpr = run.find("w:rPr", NS)
                if rpr is None:
                    rpr = etree.Element(tag("rPr"))
                    run.insert(0, rpr)
                size = rpr.find("w:sz", NS)
                if size is None:
                    size = etree.Element(tag("sz"))
                    rpr.append(size)
                size.set(tag("val"), "16")
                size_cs = rpr.find("w:szCs", NS)
                if size_cs is None:
                    size_cs = etree.Element(tag("szCs"))
                    rpr.append(size_cs)
                size_cs.set(tag("val"), "16")
            if item.filename == "word/document.xml":
                for paragraph in root.xpath(".//w:p", namespaces=NS):
                    text = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS)).strip()
                    if not text.startswith("2.1"):
                        continue
                    ppr = paragraph.find("w:pPr", NS)
                    if ppr is None:
                        continue
                    page_break = ppr.find("w:pageBreakBefore", NS)
                    if page_break is not None:
                        ppr.remove(page_break)
            if item.filename == "word/footer2.xml":
                for text_node in root.xpath(".//w:t", namespaces=NS):
                    value = text_node.text or ""
                    value = value.replace("v1.4", "v1.5")
                    value = value.replace("2026 年 9 月 8 日", "2026 年 9 月 17 日")
                    value = value.replace("2026년 9월 8일", "2026년 9월 17일")
                    text_node.text = value
            target.writestr(item, etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True))
    temp.replace(path)
    print(f"Applied {FONT} as the CJK font and updated footer metadata: {path}")
