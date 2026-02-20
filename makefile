Qur'an_Pickthall_Transliteration_Complete.pdf : en.transliteration.txt en.pickthall.txt generate_pickthall_transliteration_pdf.py
	python3 generate_pickthall_transliteration_pdf.py

farooq.pdf : farooq.tex
	xelatex farooq.tex
suhail.pdf : suhail.tex
	xelatex suhail.tex
sahih.pdf : sahih.tex
	xelatex sahih.tex
translit.pdf : translit.tex
	xelatex translit.tex
pickthall.pdf : pickthall.tex
	xelatex pickthall.tex


farooq.tex:qum.tex
suhail.tex:qup.tex
sahih.tex:qus.tex
translit.tex:qut.tex
pickthall.tex:qupk.tex

clean:
	rm -rf *.toc *.aux *.out *.log
