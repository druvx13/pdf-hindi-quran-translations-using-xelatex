#!/usr/bin/env python3
"""
Generate a combined PDF of the Tanzil.net English Transliteration and
Mohammed Marmaduke Pickthall English Translation of the Qur'an.

Output: Qur'an_Pickthall_Transliteration_Complete.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.platypus.flowables import AnchorFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---------------------------------------------------------------------------
# Surah metadata (identical to existing scripts in this repository)
# ---------------------------------------------------------------------------
SURA_SIZES = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99,
    128, 111, 110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34,
    30, 73, 54, 45, 83, 182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29,
    18, 45, 60, 49, 62, 55, 78, 96, 29, 22, 24, 13, 14, 11, 11, 18, 12,
    12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31, 50, 40, 46, 42, 29, 19,
    36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6,
]

SURA_NAMES = [
    "Al-Fatihah (The Opening)", "Al-Baqarah (The Cow)",
    "Al-'Imran (The Family of Amran)", "An-Nisa' (The Women)",
    "Al-Ma'idah (The Food)", "Al-An'am (The Cattle)",
    "Al-A'raf (The Elevated Places)", "Al-Anfal (Voluntary Gifts)",
    "Al-Bara'at / At-Taubah (The Immunity)", "Yunus (Jonah)", "Hud (Hud)",
    "Yusuf (Joseph)", "Ar-Ra'd (The Thunder)", "Ibrahim (Abraham)",
    "Al-Hijr (The Rock)", "An-Nahl (The Bee)",
    "Bani Isra'il (The Israelites)", "Al-Kahf (The Cave)", "Maryam (Mary)",
    "Ta Ha (Ta Ha)", "Al-Anbiya' (The Prophets)", "Al-Hajj (The Pilgrimage)",
    "Al-Mu'minun (The Believers)", "An-Nur (The Light)",
    "Al-Furqan (The Discrimination)", "Ash-Shu'ara' (The Poets)",
    "An-Naml (The Naml)", "Al-Qasas (The Narrative)",
    "Al-'Ankabut (The Spider)", "Ar-Rum (The Romans)", "Luqman (Luqman)",
    "As-Sajdah (The Adoration)", "Al-Ahzab (The Allies)",
    "Al-Saba' (The Saba')", "Al-Fatir (The Originator)", "Ya Sin (Ya Sin)",
    "As-Saffat (Those Ranging in Ranks)", "Sad (Sad)",
    "Az-Zumar (The Companies)", "Al-Mu'min (The Believer)",
    "Ha Mim (Ha Mim)", "Ash-Shura (Counsel)", "Az-Zukhruf (Gold)",
    "Ad-Dukhan (The Drought)", "Al-Jathiyah (The Kneeling)",
    "Al-Ahqaf (The Sandhills)", "Muhammad (Muhammad)",
    "Al-Fath (The Victory)", "Al-Hujurat (The Apartments)", "Qaf (Qaf)",
    "Ad-Dhariyat (The Scatterers)", "At-Tur (The Mountain)",
    "An-Najm (The Star)", "Al-Qamar (The Moon)",
    "Ar-Rahman (The Beneficent)", "Al-Waqi'ah (The Event)",
    "Al-Hadid (Iron)", "Al-Mujadilah (The Pleading Woman)",
    "Al-Hashr (The Banishment)",
    "Al-Mumtahanah (The Woman who is Examined)", "As-Saff (The Ranks)",
    "Al-Jumu'ah (The Congregation)", "Al-Munafiqun (The Hypocrites)",
    "At-Taghabun (The Manifestation of Losses)", "At-Talaq (Divorce)",
    "At-Tahrim (The Prohibition)", "Al-Mulk (The Kingdom)",
    "Al-Qalam (The Pen)", "Al-Haqqah (The Sure Truth)",
    "Al-Ma'arij (The Ways of Ascent)", "Nuh (Noah)", "Al-Jinn (The Jinn)",
    "Al-Muzzammil (The One Covering Himself)",
    "Al-Muddaththir (The One Wrapping Himself Up)",
    "Al-Qiyamah (The Resurrection)", "Al-Insan (The Man)",
    "Al-Mursalat (Those Sent Forth)", "An-Naba' (The Announcement)",
    "An-Nazi'at (Those Who Yearn)", "'Abasa (He Frowned)",
    "At-Takwir (The Folding Up)", "Al-Infitar (The Cleaving)",
    "At-Tatfif (Default in Duty)", "Al-Inshiqaq (The Bursting Asunder)",
    "Al-Buruj (The Stars)", "At-Tariq (The Comer by Night)",
    "Al-A'la (The Most High)", "Al-Ghashiyah (The Overwhelming Event)",
    "Al-Fajr (The Daybreak)", "Al-Balad (The City)",
    "Ash-Shams (The Sun)", "Al-Lail (The Night)",
    "Ad-Duha (The Brightness of the Day)", "Al-Inshirah (The Expansion)",
    "At-Tin (The Fig)", "Al-'Alaq (The Clot)", "Al-Qadr (The Majesty)",
    "Al-Bayyinah (The Clear Evidence)", "Al-Zilzal (The Shaking)",
    "Al-'Adiyat (The Assaulters)", "Al-Qari'ah (The Calamity)",
    "At-Takathur (The Abundance of Wealth)", "Al-'Asr (The Time)",
    "Al-Humazah (The Slanderer)", "Al-Fil (The Elephant)",
    "Al-Quraish (The Quraish)", "Al-Ma'un (Acts of Kindness)",
    "Al-Kauthar (The Abundance of Good)", "Al-Kafirun (The Disbelievers)",
    "An-Nasr (The Help)", "Al-Lahab (The Flame)", "Al-Ikhlas (The Unity)",
    "Al-Falaq (The Dawn)", "An-Nas (The Men)",
]

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
TRANSLIT_FILE = os.path.join(REPO_ROOT, "en.transliteration.txt")
PICKTHALL_FILE = os.path.join(REPO_ROOT, "en.pickthall.txt")
OUTPUT_PDF = os.path.join(REPO_ROOT, "Qur'an_Pickthall_Transliteration_Complete.pdf")


def discover_files():
    """Report found source files and raise if missing."""
    print("Scanning repository for source files …")
    for label, path in [
        ("Transliteration (Tanzil.net)", TRANSLIT_FILE),
        ("Translation (Pickthall)", PICKTHALL_FILE),
    ]:
        if os.path.isfile(path):
            print(f"  [FOUND] {label}: {path}")
        else:
            print(f"  [MISSING] {label}: {path}")
            sys.exit(1)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_file(path):
    """Return list of verse strings (one per line, UTF-8)."""
    with open(path, encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def build_data(translit_lines, pickthall_lines):
    """
    Merge two flat verse lists into a list of dicts:
        {surah, ayah, transliteration, translation}
    Logs a warning when ayah counts diverge between the files.
    """
    data = []
    t_idx = 0
    p_idx = 0
    total_t = len(translit_lines)
    total_p = len(pickthall_lines)

    for surah_num, size in enumerate(SURA_SIZES, start=1):
        for ayah_num in range(1, size + 1):
            translit = translit_lines[t_idx] if t_idx < total_t else ""
            pickthall = pickthall_lines[p_idx] if p_idx < total_p else ""
            if t_idx >= total_t:
                print(
                    f"  [WARN] Missing transliteration for {surah_num}:{ayah_num}"
                )
            if p_idx >= total_p:
                print(
                    f"  [WARN] Missing translation for {surah_num}:{ayah_num}"
                )
            data.append(
                {
                    "surah": surah_num,
                    "ayah": ayah_num,
                    "transliteration": translit,
                    "translation": pickthall,
                }
            )
            t_idx += 1
            p_idx += 1

    return data


def validate(translit_lines, pickthall_lines):
    """Integrity checks: surah count, encoding, total ayah count."""
    total_expected = sum(SURA_SIZES)
    print(f"\nIntegrity Check:")
    print(f"  Expected surahs   : 114")
    print(f"  Expected ayahs    : {total_expected}")
    print(f"  Transliteration   : {len(translit_lines)} lines")
    print(f"  Pickthall         : {len(pickthall_lines)} lines")
    if len(translit_lines) != total_expected:
        print(
            f"  [WARN] Transliteration line count ({len(translit_lines)}) "
            f"!= expected ({total_expected})"
        )
    if len(pickthall_lines) != total_expected:
        print(
            f"  [WARN] Pickthall line count ({len(pickthall_lines)}) "
            f"!= expected ({total_expected})"
        )


# ---------------------------------------------------------------------------
# PDF generation helpers
# ---------------------------------------------------------------------------

PAGE_WIDTH, PAGE_HEIGHT = 6 * inch, 9 * inch   # 6 × 9 standard book size
MARGIN = 1 * inch


def _footer(canvas, doc):
    """Draw page number centred in the footer."""
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    page_text = str(doc.page)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, 0.5 * inch, page_text)
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()

    surah_heading = ParagraphStyle(
        "SurahHeading",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        spaceAfter=6,
        spaceBefore=18,
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
    )

    translit_style = ParagraphStyle(
        "Transliteration",
        fontName="Courier-Bold",
        fontSize=10,
        leading=14,
        spaceAfter=2,
        spaceBefore=4,
        textColor=colors.HexColor("#003366"),
    )

    translation_style = ParagraphStyle(
        "Translation",
        fontName="Times-Roman",
        fontSize=11,
        leading=15,
        spaceAfter=6,
        leftIndent=12,
        textColor=colors.black,
    )

    toc_style = ParagraphStyle(
        "TOCEntry",
        fontName="Times-Roman",
        fontSize=10,
        leading=14,
    )

    return surah_heading, translit_style, translation_style, toc_style


# ---------------------------------------------------------------------------
# Main PDF builder
# ---------------------------------------------------------------------------

def build_pdf(data):
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 0.25 * inch,  # extra room for page numbers
        title="Qur'an – Pickthall Translation & Tanzil Transliteration",
        author="Mohammed Marmaduke Pickthall / Tanzil.net",
        subject="Qur'an in English Translation and Transliteration",
    )

    surah_heading_style, translit_style, translation_style, _ = build_styles()

    # Build a manual TOC page as plain text then switch to story
    story = []

    # ---- Title page --------------------------------------------------------
    title_style = ParagraphStyle(
        "Title",
        fontName="Times-Bold",
        fontSize=20,
        leading=28,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a2e"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName="Times-Roman",
        fontSize=13,
        leading=18,
        spaceAfter=8,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"),
    )

    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("The Holy Qur'an", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "English Translation by Mohammed Marmaduke Pickthall", subtitle_style
        )
    )
    story.append(
        Paragraph(
            "with Romanized Transliteration by Tanzil.net", subtitle_style
        )
    )
    story.append(PageBreak())

    # ---- Table of Contents (clickable) ------------------------------------
    toc_title_style = ParagraphStyle(
        "TOCTitle",
        fontName="Times-Bold",
        fontSize=16,
        leading=22,
        spaceAfter=16,
        alignment=TA_CENTER,
    )
    toc_entry_style = ParagraphStyle(
        "TOCEntry",
        fontName="Times-Roman",
        fontSize=9,
        leading=13,
        leftIndent=0,
    )

    story.append(Paragraph("Table of Contents", toc_title_style))
    story.append(Spacer(1, 0.1 * inch))

    for idx, name in enumerate(SURA_NAMES, start=1):
        anchor_name = f"surah_{idx}"
        link_text = (
            f'<a href="#{anchor_name}" color="#003366">'
            f'{idx:3d}. {name}'
            f'</a>'
        )
        story.append(Paragraph(link_text, toc_entry_style))

    story.append(PageBreak())

    # ---- Body: Surahs & Ayahs ---------------------------------------------
    ayah_idx = 0

    for surah_num, size in enumerate(SURA_SIZES, start=1):
        name = SURA_NAMES[surah_num - 1]
        anchor_name = f"surah_{surah_num}"

        # Surah anchor + heading
        story.append(AnchorFlowable(anchor_name))
        story.append(
            Paragraph(
                f"Surah {surah_num}: {name}", surah_heading_style
            )
        )
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 0.08 * inch))

        for ayah_num in range(1, size + 1):
            verse = data[ayah_idx]
            ayah_idx += 1

            # Ayah number + transliteration
            translit_text = (
                f'<b>[{surah_num}:{ayah_num}]</b>  {verse["transliteration"]}'
            )
            story.append(Paragraph(translit_text, translit_style))

            # Translation
            story.append(Paragraph(verse["translation"], translation_style))
            story.append(Spacer(1, 0.05 * inch))

        story.append(PageBreak())

    print(f"\nBuilding PDF: {OUTPUT_PDF}")
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    print(f"Done. Output saved to: {OUTPUT_PDF}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    discover_files()

    print("\nParsing source files …")
    translit_lines = parse_file(TRANSLIT_FILE)
    pickthall_lines = parse_file(PICKTHALL_FILE)

    validate(translit_lines, pickthall_lines)

    print("\nMerging data …")
    data = build_data(translit_lines, pickthall_lines)
    print(f"  Total verses merged: {len(data)}")

    build_pdf(data)


if __name__ == "__main__":
    main()
