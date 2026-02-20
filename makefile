farooq.pdf : farooq.tex
	xelatex farooq.tex
suhail.pdf : suhail.tex
	xelatex suhail.tex
sahih.pdf : sahih.tex
	xelatex sahih.tex
translit.pdf : translit.tex
	xelatex translit.tex


farooq.tex:qum.tex
suhail.tex:qup.tex
sahih.tex:qus.tex
translit.tex:qut.tex

clean:
	rm -rf *.toc *.aux *.out *.log
