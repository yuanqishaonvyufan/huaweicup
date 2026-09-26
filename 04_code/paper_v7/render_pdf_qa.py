"""Render every PDF page for the final visual audit."""

import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("pdf", type=Path)
    p.add_argument("--prefix", required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(args.pdf))
    cards = []
    for i, page in enumerate(doc):
        image = page.render(scale=1).to_pil().convert("RGB")
        canvas = Image.new("RGB", (int(image.width * 0.55), int(image.height * 0.55) + 30), "white")
        small = image.resize((canvas.width, canvas.height - 30))
        canvas.paste(small, (0, 30))
        ImageDraw.Draw(canvas).text((8, 8), f"Page {i+1}", fill="black")
        cards.append(canvas)
        if i+1 in {3, 45, 46, 48, 49, 50, 51, 52, 53}:
            page.render(scale=1.65).to_pil().save(args.out / f"{args.prefix}_page_{i+1:02d}.png")
    for offset in range(0, len(cards), 4):
        group = cards[offset:offset+4]
        sheet = Image.new("RGB", (max(x.width for x in group)*4, max(x.height for x in group)), "#dddddd")
        for j, card in enumerate(group):
            sheet.paste(card, (j*card.width, 0))
        sheet.save(args.out / f"{args.prefix}_sheet_{offset//4+1:02d}.png")
    print(f"pages={len(doc)} sheets={(len(cards)+3)//4}")


if __name__ == "__main__":
    main()
