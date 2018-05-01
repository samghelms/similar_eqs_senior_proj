# Intro

This repository contains work I have done for my senior thesis to identify similar equations written in latex.

# Testing

run `pytest` (pip install it if you don't have it)
# Todos

1. Finish up tests and set up pytest

2. Deal with lone operators

3. why is this happening? \n-\zeta(2) 

# Stoplist

[\left, \right, \mbox, \begin{aligned}, \begin{*}, \end{*}, \ensuremath]

# Important 

## WARNING WARNING!!! MAKE SURE YOU SAVE YOUR FILE IN UTF-8. OPEN THE FILE IN UTF-8. YOU WILL FAIL OTHERWISE.

# Improvements

Currently, it doesn't parse any sort of matrix or array alignment type, such as `array` or `pmatrix`. These are used surprisingly frequently to align equations.

nasty example:

\n\xymatrix@R=0.25cm @C=0.7cm{\nU \otimes (V \otimes W) \ar[r]^{c_{U,V \otimes W}}(V \otimes W) \otimes U \ar[dr]^{\alpha_{V,W,U}}\\\n(U \otimes V) \otimes W \ar[dr]_-{c_{U,V} \otimes W} \ar[ur]^{\alpha_{U,V,W}}V \otimes (W \otimes U)\\\n(V \otimes U) \otimes W \ar[r]_{\alpha_{V,U,W}}V \otimes (U \otimes W)\ar[ur]_{ V \otimes c_{U,W}}\n}\n


''\\nA'' versus '\\nabla'

\\begin{equation}\n 3\\widetilde{\\Gamma}_{2j}-3\\Gamma_{2j}=-3R_4(0)a_{2j}^2 -6\\int_{\\gamma_j}\\frac{S_2R_4}{r^5}\\,\\psi_2\\varphi_1^4\\,dw +3\\int_{\\gamma_j}\\frac{S_2R_3}{r^4}\\,\\psi_2^2\\varphi_1^3\\,dw.\n\\end{equation}


sometimes people use \\, to denote spacing

# pitfalls
Sometimes people don't put a space between macros and variables: *\betaz* should be \beta z. But most math renderers won't fix this for you anyways, so I will consider this a bug.
\mathrm{or,}\sqrt{\alpha^2-\beta^2}-c=-\betaz+\alpha\sqrt{1+z^2}

x=e^{-w}, 
z=\sum_{\mu=1}^\infty
\frac{\mu^{\mu-1}}{\mu!}\;e^{-\mu}\;x^\mu,
t-1=\sum_{\mu=1}^\infty
\frac{\mu^{\mu}}{\mu!}\;e^{-\mu}\;x^\mu.

Only "t-1=\sum_{\mu=1}^\infty \frac{\mu^{\mu}}{\mu!}\;e^{-\mu}\;x^\mu." gets pulled out because of the t-1. To keep the parsers simple, I propose dealing with this with a simple tf-idf pass, rather than with the parser rules.

# Interesting examples

This is correct: \mathrm{or,}\sqrt{\alpha^2-\beta^2}-c=-\betaz+\alpha\sqrt{1+z^2}

(you could filter out tags like mathrm and text later)

tags you might want to filter: mathrm, text, mbox

Why we should keep text tags? 

\bigcup_{i \in I} \Omega_i : {\mathcal{X}} {\dashrightarrow} {\mathcal{Y}},  \left( \bigcup_{i \in I} \Omega_i \right)(x):=
\bigcup_{i \in I} \Omega_i(x) \text{ for all } x \in {\mathcal{X}}.

# Things you may want to further filter:

"\\;" and "\\,"

# Todos:

1. \\text \\mbox
2. make right/left dependency configurable
3. add \\textrm to high level splits
4. add [textstyle] to stoplist
5. "fold" aligns with nothing on LHS in.
6. make all rules configurable
7. maybe get rid of the fraction?
8. bring in some sort of hash table of latex symbols?
9. deal with: \log\psi(t)=\int_{-\infty}^{0}\left(e^{itx}-1-itx\right)\frac{\alpha dx}{|x|^{\alpha+1}}=-C_{\alpha}|t|^{\alpha}\left(1+i(1+i\  \text{\e m sgn}(t)\tan\frac{\pi\alpha}{2}\right
10. add in rule for lone fractions?
11. add periods to stoplist options -- build in a rule to not mess with decimals
12. allow numbers to be of one string
13. deal with: \sum_{k}\theta(n+k,n)\frac{u^{n+k}}{(n+k)!}=\sum_{k}\frac{(n+k)!}{(n-1)!}\delta_k(n+k)\frac{u^{n+k}}{(n+k)!}=\frac{1}{n!}\arg\tanhnu,
14. add paranthesis to dependents again? and maybe brackets? For function definitions: \sum_{k}\theta(n+k,n)\frac{u^{n+k}}{(n+k)!}=\sum_{k}\frac{(n+k)!}{(n-1)!}\delta_k(n+k)\frac{u^{n+k}}{(n+k)!}=\frac{1}{n!}\arg\tanhnu,
15. K_T = \frac{(1-\gamma) \log(Tt^2)}{K(\theta_a^*-t,\theta_a^*+\zeta t)} = \frac{(1-\gamma) \log(Tt^2)}{K(\overline{\theta}_a,\theta_a^*+\zetat)},
16. Write an example of how to filter out partials

list of all mathematical symbols:

https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols

http://tug.ctan.org/info/symbols/comprehensive/symbols-a4.pdf


Based right and left dependency rules off of this: http://web.ift.uib.no/Teori/KURS/WRK/TeX/symALL.html

tokenize makes two passes:

first, to chunk up everything, second to split macros like \\betadx => \\beta dx