#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate /docs HTML pages for the Qur'an website.

Sources used:
  - trans/en.transliteration.txt  : sura|ayah|transliteration (with HTML tags)
  - quran_hindi_farooq.txt        : [sura:ayah] Hindi translation (Farooq Khan)
  - en.pickthall.txt              : one English line per ayah (Pickthall)
"""

import os
import re

# ---------------------------------------------------------------------------
# Surah metadata
# ---------------------------------------------------------------------------
SURA_SIZE = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,
             110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,
             182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,
             29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,
             40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,
             11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

SURA_NAME = [
    "Al-Fatihah (The Opening)","Al-Baqarah (The Cow)",
    "Al-'Imran (The Family of Amran)","An-Nisa' (The Women)",
    "Al-Ma'idah (The Food)","Al-An'am (The Cattle)",
    "Al-A'raf (The Elevated Places)","Al-Anfal (Voluntary Gifts)",
    "Al-Bara'at / At-Taubah(The Immunity)","Yunus (Jonah)","Hud (Hud)",
    "Yusuf (Joseph)","Ar-Ra'd (The Thunder)","Ibrahim (Abraham)",
    "Al-Hijr (The Rock)","An-Nahl (The Bee)","Bani Isra'il (The Israelites)",
    "Al-Kahf (The Cave)","Maryam (Mary)","Ta Ha (Ta Ha)",
    "Al-Anbiya' (The Prophets)","Al-Hajj (The Pilgrimage)",
    "Al-Mu'minun (The Believers)","An-Nur (The Light)",
    "Al-Furqan (The Discrimination)","Ash-Shu'ara' (The Poets)",
    "An-Naml (The Naml)","Al-Qasas (The Narrative)",
    "Al-'Ankabut (The Spider)","Ar-Rum (The Romans)","Luqman (Luqman)",
    "As-Sajdah (The Adoration)","Al-Ahzab (The Allies)",
    "Al-Saba' (The Saba')","Al-Fatir (The Originator)","Ya Sin (Ya Sin)",
    "As-Saffat (Those Ranging in Ranks)","Sad (Sad)",
    "Az-Zumar (The Companies)","Al-Mu'min (The Believer)","Ha Mim (Ha Mim)",
    "Ash-Shura (Counsel)","Az-Zukhruf (Gold)","Ad-Dukhan (The Drought)",
    "Al-Jathiyah (The Kneeling)","Al-Ahqaf (The Sandhills)",
    "Muhammad (Muhammad)","Al-Fath (The Victory)",
    "Al-Hujurat (The Apartments)","Qaf (Qaf)",
    "Ad-Dhariyat (The Scatterers)","At-Tur (The Mountain)",
    "An-Najm (The Star)","Al-Qamar (The Moon)",
    "Ar-Rahman (The Beneficent)","Al-Waqi'ah (The Event)",
    "Al-Hadid (Iron)","Al-Mujadilah (The Pleading Woman)",
    "Al-Hashr (The Banishment)",
    "Al-Mumtahanah (The Woman who is Examined)","As-Saff (The Ranks)",
    "Al-Jumu'ah (The Congregation)","Al-Munafiqun (The Hypocrites)",
    "At-Taghabun (The Manifestation of Losses)","At-Talaq (Divorce)",
    "At-Tahrim (The Prohibition)","Al-Mulk (The Kingdom)",
    "Al-Qalam (The Pen)","Al-Haqqah (The Sure Truth)",
    "Al-Ma'arij (The Ways of Ascent)","Nuh (Noah)","Al-Jinn (The Jinn)",
    "Al-Muzzammil (The One Covering Himself)",
    "Al-Muddaththir (The One Wrapping Himself Up)",
    "Al-Qiyamah (The Resurrection)","Al-Insan (The Man)",
    "Al-Mursalat (Those Sent Forth)","An-Naba' (The Announcement)",
    "An-Nazi'at (Those Who Yearn)","'Abasa (He Frowned)",
    "At-Takwir (The Folding Up)","Al-Infitar (The Cleaving)",
    "At-Tatfif (Default in Duty)","Al-Inshiqaq (The Bursting Asunder)",
    "Al-Buruj (The Stars)","At-Tariq (The Comer by Night)",
    "Al-A'la (The Most High)","Al-Ghashiyah (The Overwhelming Event)",
    "Al-Fajr (The Daybreak)","Al-Balad (The City)","Ash-Shams (The Sun)",
    "Al-Lail (The Night)","Ad-Duha (The Brightness of the Day)",
    "Al-Inshirah (The Expansion)","At-Tin (The Fig)",
    "Al-'Alaq (The Clot)","Al-Qadr (The Majesty)",
    "Al-Bayyinah (The Clear Evidence)","Al-Zilzal (The Shaking)",
    "Al-'Adiyat (The Assaulters)","Al-Qari'ah (The Calamity)",
    "At-Takathur (The Abundance of Wealth)","Al-'Asr (The Time)",
    "Al-Humazah (The Slanderer)","Al-Fil (The Elephant)",
    "Al-Quraish (The Quraish)","Al-Ma'un (Acts of Kindness)",
    "Al-Kauthar (The Abundance of Good)","Al-Kafirun (The Disbelievers)",
    "An-Nasr (The Help)","Al-Lahab (The Flame)","Al-Ikhlas (The Unity)",
    "Al-Falaq (The Dawn)","An-Nas (The Men)",
]

# ---------------------------------------------------------------------------
# Load transliteration  trans/en.transliteration.txt
# Format: sura|ayah|text_with_html_tags  (comment lines start with #)
# ---------------------------------------------------------------------------
translit = {}
with open('trans/en.transliteration.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        parts = line.split('|', 2)
        if len(parts) == 3:
            translit[(int(parts[0]), int(parts[1]))] = parts[2]

# ---------------------------------------------------------------------------
# Load Hindi translation  quran_hindi_farooq.txt
# Format: [sura:ayah] text
# ---------------------------------------------------------------------------
hindi = {}
with open('quran_hindi_farooq.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        m = re.match(r'^\[(\d+):(\d+)\]\s*(.*)', line)
        if m:
            hindi[(int(m.group(1)), int(m.group(2)))] = m.group(3)

# ---------------------------------------------------------------------------
# Load Pickthall translation  en.pickthall.txt  (sequential, one line/ayah)
# ---------------------------------------------------------------------------
pickthall = {}
with open('en.pickthall.txt', 'r', encoding='utf-8') as f:
    for sura_idx, size in enumerate(SURA_SIZE, 1):
        for ayah in range(1, size + 1):
            pickthall[(sura_idx, ayah)] = f.readline().rstrip('\n')

# ---------------------------------------------------------------------------
# HTML template helpers
# ---------------------------------------------------------------------------
CSS = """\
*,*::before,*::after{box-sizing:border-box}
body{margin:0;padding:0;font-family:system-ui,Arial,Helvetica,sans-serif;
  font-size:16px;background:#fff;color:#111;line-height:1.6}
header{background:#1a3a5c;color:#fff;padding:12px 16px;position:sticky;top:0;z-index:10}
header a{color:#ffd54f;text-decoration:none;font-weight:bold;font-size:1.1em}
header a:hover{text-decoration:underline}
main{padding:16px;max-width:900px;margin:0 auto}
h1{font-size:1.4em;margin:0 0 12px}
h2{font-size:1.2em;color:#1a3a5c;margin:20px 0 8px}
.surah-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;margin-top:16px}
.surah-grid a{display:block;padding:10px 12px;background:#f0f4f8;border:1px solid #ccd6e0;
  border-radius:6px;text-decoration:none;color:#1a3a5c;font-size:.95em}
.surah-grid a:hover{background:#dde8f2}
.notice{background:#fff8e1;border-left:4px solid #ffd54f;padding:12px 16px;margin-bottom:20px;font-size:.95em}
.table-wrap{overflow-x:auto;width:100%}
table{width:100%;border-collapse:collapse;margin-bottom:24px}
th{background:#1a3a5c;color:#fff;padding:10px 12px;text-align:left;font-size:.9em}
td{padding:10px 12px;vertical-align:top;border:1px solid #ccd6e0}
tr:nth-child(odd) td{background:#f9fbfd}
.ayah-num{color:#888;font-size:.85em;min-width:42px;white-space:nowrap}
.translit{font-style:normal;font-weight:600}
.hindi{font-family:'Noto Sans Devanagari',Arial,sans-serif;color:#3a2a6c}
nav.chapter-nav{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;
  padding:16px 0;margin-top:8px;border-top:1px solid #ccd6e0}
nav.chapter-nav a{display:inline-block;padding:8px 16px;background:#1a3a5c;color:#fff;
  border-radius:4px;text-decoration:none;font-size:.95em}
nav.chapter-nav a:hover{background:#2a5a8c}
footer{text-align:center;padding:20px;font-size:.85em;color:#666;border-top:1px solid #e0e0e0;margin-top:32px}"""

HEADER_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Surah {num}: {name}</title>
<style>
{css}
</style>
</head>
<body>
<header><a href="index.html">&#8962; Index</a></header>
<main>
<h1>Surah {num}: {name}</h1>
<div class='table-wrap'><table><thead><tr><th>#</th><th>Transliteration (Tanzil.net)</th><th>Translation (Pickthall)</th><th>&#2361;&#2367;&#2344;&#2381;&#2342;&#2368; &#2309;&#2344;&#2369;&#2357;&#2366;&#2342; (Farooq Khan)</th></tr></thead><tbody>
"""

FOOTER_HTML = """\
</tbody></table></div>
{nav}
</main>
<footer>Tanzil.net Transliteration &amp; Pickthall Translation &mdash; Public Domain &nbsp;|&nbsp; Hindi: Farooq Khan &amp; Muhammad Ahmed</footer>
</body>
</html>"""

# ---------------------------------------------------------------------------
# Generate surah HTML files
# ---------------------------------------------------------------------------
docs_dir = 'docs'
os.makedirs(docs_dir, exist_ok=True)

for sura_idx in range(1, 115):
    size = SURA_SIZE[sura_idx - 1]
    name = SURA_NAME[sura_idx - 1]
    filename = os.path.join(docs_dir, '%03d.html' % sura_idx)

    prev_link = ''
    next_link = ''
    if sura_idx > 1:
        prev_link = "<a href='%03d.html'>&laquo; Surah %d</a>" % (sura_idx - 1, sura_idx - 1)
    if sura_idx < 114:
        next_link = "<a href='%03d.html'>Surah %d &raquo;</a>" % (sura_idx + 1, sura_idx + 1)
    nav = "<nav class='chapter-nav'><span>%s</span><span>%s</span></nav>" % (prev_link, next_link)

    with open(filename, 'w', encoding='utf-8') as out:
        out.write(HEADER_HTML.format(num=sura_idx, name=name, css=CSS))
        for ayah in range(1, size + 1):
            tl = translit.get((sura_idx, ayah), '')
            pk = pickthall.get((sura_idx, ayah), '')
            hi = hindi.get((sura_idx, ayah), '')
            out.write(
                "<tr>"
                "<td class='ayah-num'>%d</td>"
                "<td class='translit'>%s</td>"
                "<td class='trans'>%s</td>"
                "<td class='hindi'>%s</td>"
                "</tr>\n" % (ayah, tl, pk, hi)
            )
        out.write(FOOTER_HTML.format(nav=nav))

    print('Written: %s' % filename)

# ---------------------------------------------------------------------------
# Regenerate index.html
# ---------------------------------------------------------------------------
index_path = os.path.join(docs_dir, 'index.html')
with open(index_path, 'w', encoding='utf-8') as out:
    out.write("""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Qur'an &ndash; Transliteration &amp; Translation</title>
<style>
%s
</style>
</head>
<body>
<header><a href="index.html">&#8962; Index</a></header>
<main>
<h1>Qur&#x2019;an &mdash; Transliteration, English &amp; Hindi Translation</h1>
<div class="notice">
<strong>Public Domain Notice &amp; Source Attribution</strong><br>
<em>Transliteration:</em> Tanzil.net English Transliteration of the Qur&#x2019;an.<br>
<em>English Translation:</em> Mohammed Marmaduke Pickthall, <em>The Meaning of the Glorious Koran</em> (1930) &mdash; Public Domain.<br>
<em>Hindi Translation (&#2361;&#2367;&#2344;&#2381;&#2342;&#2368; &#2309;&#2344;&#2369;&#2357;&#2366;&#2342;):</em> Muhammad Farooq Khan &amp; Muhammad Ahmed.<br>
Texts are reproduced verbatim; no alterations have been made.
</div>
<h2>Surahs (Chapters)</h2>
<div class="surah-grid">
""" % CSS)
    for i, name in enumerate(SURA_NAME, 1):
        out.write("<a href='%03d.html'><strong>%d.</strong> %s</a>\n" % (i, i, name))
    out.write("""\
</div>
</main>
<footer>Tanzil.net Transliteration &amp; Pickthall Translation &mdash; Public Domain &nbsp;|&nbsp; Hindi: Farooq Khan &amp; Muhammad Ahmed</footer>
</body>
</html>""")

print('Written: %s' % index_path)
print('Done. %d surah files + index regenerated.' % 114)
