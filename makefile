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
translit_pickthall.pdf : translit_pickthall.tex
	xelatex translit_pickthall.tex


farooq.tex:qum.tex
suhail.tex:qup.tex
sahih.tex:qus.tex
translit.tex:qut.tex
pickthall.tex:qupk.tex
translit_pickthall.tex:qutpk.tex

clean:
	rm -rf *.toc *.aux *.out *.log
