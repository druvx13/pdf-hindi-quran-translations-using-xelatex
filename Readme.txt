This is the xelatex compiled pdf for Hindi and English Translations of Quran
written by

1)Muhammad Farooq Khan and Muhammad Ahmed
2)Suhel Farooq Khan and Saifur Rahman Nadwi
3)Saheeh International (English)
4)Tanzil.net (English Transliteration)
5)Mohammed Marmaduke Pickthall (English)


The text form of translations are downloaded from [www.zekr.org] and [tanzil.net]


gentextforquran.py is to be run to generate the tex files


xelatex farooq.tex 

gives farooq.pdf which is Muhammad Farooq Khan and Muhammad Ahmed's quran translation

xelatex suhail.tex 

gives suhail.pdf which is Suhel Farooq Khan and Saifur Rahman Nadwi's quran translation

xelatex sahih.tex

gives sahih.pdf which is Saheeh International's English Quran translation

xelatex translit.tex

gives translit.pdf which is the English Transliteration of the Quran (Tanzil.net)

xelatex pickthall.tex

gives pickthall.pdf which is Mohammed Marmaduke Pickthall's English Quran translation

xelatex translit_pickthall.tex

gives translit_pickthall.pdf which is a combined PDF containing:
  - English Transliteration (Tanzil.net) in italics
  - English Translation by Mohammed Marmaduke Pickthall
For each verse: the Arabic text is shown right-aligned, followed by the transliteration
and the Pickthall translation, separated by a thin rule for easy reading.


gentxtforquran.py is to be run to generate formatted plain-text versions:
  quran_hindi_farooq.txt      - Hindi translation by Muhammad Farooq Khan and Muhammad Ahmed
  quran_hindi_suhail.txt      - Hindi translation by Suhel Farooq Khan and Saifur Rahman Nadwi
  quran_english_sahih.txt     - English translation by Saheeh International
  quran_english_translit.txt  - English Transliteration (Tanzil.net)
  quran_english_pickthall.txt - English translation by Mohammed Marmaduke Pickthall

