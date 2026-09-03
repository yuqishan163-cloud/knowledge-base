#!/usr/bin/env python3
"""Extract EPUB spine documents to readable text plus a coverage manifest."""

from __future__ import annotations

import argparse
import html
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote
from xml.etree import ElementTree as ET


class TextExtractor(HTMLParser):
    BLOCKS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "section"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"}:
            self.skip += 1
        elif not self.skip and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg"} and self.skip:
            self.skip -= 1
        elif not self.skip and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts)).replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n[ \t]+", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def resolve(base: str, href: str) -> str:
    clean_href = unquote(href.split("#", 1)[0])
    return str(PurePosixPath(base).parent.joinpath(clean_href))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.epub) as archive:
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        rootfile = next(e.attrib["full-path"] for e in container.iter() if local_name(e.tag) == "rootfile")
        package = ET.fromstring(archive.read(rootfile))

        metadata: dict[str, str] = {}
        for element in package.iter():
            name = local_name(element.tag)
            if name in {"title", "creator", "language", "identifier"} and element.text and name not in metadata:
                metadata[name] = element.text.strip()

        manifest = {
            e.attrib["id"]: resolve(rootfile, e.attrib["href"])
            for e in package.iter()
            if local_name(e.tag) == "item" and "id" in e.attrib and "href" in e.attrib
        }
        spine_ids = [e.attrib["idref"] for e in package.iter() if local_name(e.tag) == "itemref" and "idref" in e.attrib]

        documents = []
        for index, item_id in enumerate(spine_ids, start=1):
            source = manifest.get(item_id)
            if not source:
                continue
            try:
                raw = archive.read(source).decode("utf-8", errors="replace")
            except KeyError:
                continue
            parser = TextExtractor()
            parser.feed(raw)
            extracted = parser.text()
            filename = f"{index:04d}.txt"
            (args.output_dir / filename).write_text(extracted, encoding="utf-8")
            documents.append({"index": index, "id": item_id, "source": source, "output": filename, "characters": len(extracted)})

    result = {"source": str(args.epub.resolve()), "metadata": metadata, "spine_count": len(spine_ids), "documents": documents}
    (args.output_dir / "manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output_dir": str(args.output_dir.resolve()), "documents": len(documents), "characters": sum(d["characters"] for d in documents)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
