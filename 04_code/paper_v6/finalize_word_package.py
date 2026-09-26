"""Anonymize the Word-normalized package without rewriting document XML."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(".finalizing.docx")
    with ZipFile(source) as src, ZipFile(temp, "w", ZIP_DEFLATED) as dst:
        for item in src.infolist():
            if item.filename.startswith("docProps/thumbnail."):
                continue
            data = src.read(item.filename)
            if item.filename == "docProps/core.xml":
                root = etree.fromstring(data)
                ns = {"dc": "http://purl.org/dc/elements/1.1/",
                      "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"}
                for xpath in ("dc:creator", "cp:lastModifiedBy"):
                    for element in root.xpath(xpath, namespaces=ns):
                        element.text = None
                data = etree.tostring(root, encoding="UTF-8", xml_declaration=True,
                                      standalone=True)
            elif item.filename == "_rels/.rels":
                root = etree.fromstring(data)
                for rel in list(root):
                    if "metadata/thumbnail" in rel.get("Type", ""):
                        root.remove(rel)
                data = etree.tostring(root, encoding="UTF-8", xml_declaration=True,
                                      standalone=True)
            elif item.filename == "[Content_Types].xml":
                root = etree.fromstring(data)
                for part in list(root):
                    if "thumbnail" in part.get("PartName", "").lower():
                        root.remove(part)
                data = etree.tostring(root, encoding="UTF-8", xml_declaration=True,
                                      standalone=True)
            dst.writestr(item, data)
    temp.replace(output)
    print(output)


if __name__ == "__main__":
    main()
