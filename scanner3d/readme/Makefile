all: pdf_latex

pdf_latex:
	@pdflatex beaudossier.tex
	@pdflatex beaudossier.tex
	@make clean

affiche:
	@evince beaudossier.pdf &

clean:
	@rm -f *.aux
	@rm -f *.fdb_latexmk
	@rm -f *.fls
	@rm -f *.log
	@rm -f *.lyx