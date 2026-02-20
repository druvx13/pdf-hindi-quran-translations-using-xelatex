farooq.pdf : farooq.tex
	xelatex farooq.tex
suhail.pdf : suhail.tex
	xelatex suhail.tex
sahih.pdf : sahih.tex
	xelatex sahih.tex


farooq.tex:qum.tex
suhail.tex:qup.tex
sahih.tex:qus.tex

clean:
	rm -rf *.toc *.aux *.out *.log
