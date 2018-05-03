# script to create the report pdf
# pandoc -t latex -s arch_280_paper.md > arch_280_paper.tex

pandoc --toc --standalone --bibliography=bibliography.bib ./writeup.md -s -o writeup.tex

../../../tectonic/target/debug/tectonic ./writeup.tex
