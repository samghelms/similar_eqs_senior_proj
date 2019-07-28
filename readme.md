# Intro

This repository contains work I have done for my senior thesis to identify similar equations written in latex.

You can read the formal writeup [here](./report/writeup.pdf).

## Motivation

Word and sentence embeddings are an incredibly powerful tool for natural language processing. Google Translate's error rate decreased by over 50\% when it switched to a model that used embeddings for translations [@noauthor_neural_nodate.

The options for telling how good embeddings are before running them through a downstream task like Google Translate are less amazing, however: Researchers only have a few small datasets, which are largely based on linguistic survey data, for this task [@schnabel_evaluation_2015].  

One of the reason so few datasets for evaluating embeddings exist are difficulties in determining when two words or sentences are different or similar. Consider how difficult it is for a machine learning model to determine that the phrase "the red-faced man" can be equivalent to "the embarrassed man" in the right context.

Mathematics is a type of language without this type of ambiguity about whether two clauses mean the same thing. The equals sign tells us with certainty when two expressions are equivalent to each other. Therefore mathematics is a perfect test bed for new embeddings models, since every mathematics text contains tens or hundreds of equivalencies with which to evaluate embeddings. 

As far as I am aware, no one has yet taken advantage of the equals sign for creating and evaluating embeddings. Throughout the course of this semester, I have created the first ever dataset of equivalent equations.

## Applications

This project will enable researchers and data scientists who work with mathematics texts to evaluate the intrinsic success of their embeddings. It may also enable better understanding of embedding in general. If I am able to create a large enough dataset of equivalent equations, the equivalent equations could also be used to train embeddings in a supervised fashion.

## Background
This fall, I started working with a research group that Prof. John Lafferty helped found called [The Hopper Project](https://github.com/hopper-project). The Hopper Project has created a dataset of academic articles from arxiv and coded up a pipeline that extracts LaTeX from these academic articles. I will extract equivalent equations from this dataset.

## Outcome: What I've Actually Created

### A dataset of equations related by things like equals signs

You can get a premade dataset of with 5 million equations in it at [https://github.com/samghelms/similar_eqs_senior_proj](https://github.com/samghelms/similar_eqs_senior_proj), in the `all_eqs` folder. This is a folder of files with processed equations. The repository includes examples on how to read in and work with these files, and instructions on how to generate your own dataset of interesting equation pairs.

These equations can be useful for a myriad of tasks, such as evaluating embeddings -- pairs split by relations should be equivalent in some sense -- or training embeddings models themselves. The final dataset has millions of equations, so the data can easily be used for such a task.

### A set of scripts for tokenizing TeX and identifying useful equations

If you're reading this report on github, you probably already know this. 

The repository at [https://github.com/samghelms/similar_eqs_senior_proj](https://github.com/samghelms/similar_eqs_senior_proj) contains the library of scripts and instructions on how to use them, as well as a premade pipeline for processing TeX formulas. Every function is unit tested and has been reworked many times based on feedback from Hopper Project researchers and mistakes made in processing jobs.

### A suite of tools for working with equation embeddings

Equations texts are harder to work with than normal english texts because they are written in LaTeX. I started working on a set of tools for visualizing mathematics in embeddings models this fall [@samghelms_mathviz:_2017]. 

This evolved into seeing how I contribute and work within existing tools. I've since come up with ways of rendering rich html/javascript representations of math in jupyter notebooks, and I have made a gist showing how to do so available to the public: [https://github.com/samghelms/similar_eqs_senior_proj](https://gist.github.com/samghelms/d1bd0a941c29044d6baa213ad96daa67).

I also got interested in being able to visualize math on T-SNE plots (for the uninitiated: a 2d scatter plot that approximates high dimensional vectors). I'm currently developing a fully fledged library that allows you to easily create such plots, and you can see my prototype in action here: [https://samghelms.github.io/webgl-scatter/](https://samghelms.github.io/webgl-scatter/) (zoom in and hover!).

# The Code

In this section, I will go over the code I have written to tokenize TeX equations at a high level and explain why I wrote it the way I did. Note that this is only a high level discussion: look to the readme and comments in the code base for specific instructions on how to use the pipeline. Before I jump into the specifics of the code, I will give a brief background on TeX to make it clearer why I had to go to the lengths I did to get aligned few math equations. 

Identifying and using equal equations in machine learning models requires two things: One, being able to properly identify tokens (so that the LaTeX code `\\int` is treated as an atomic unit and not a sequence of the characters "\\", "i", "n", and "t"); Two, being able to say whether a subexpression is substantive enough to use in the model. 

You could determine substantiveness (the second requirement) by doing things like setting a string length cutoff for the subexpression and taking tf-idf scores between two expressions on either side of an equals, but this provides no guarantee of substantiveness--the expression `x + y` is arguably just as substantive as `\\frac { x_7 } { y_i }`, with one operator and two variables, but it would be hard to determine so based on tf-idf score or the length of the expression.

As a result of this difficulty in determining substantiveness, I decided to implement a heuristic function that would make a shallow parse of the TeX expression and determine if it contained at least one operator and two variables and/or numbers at a high level. I arbitrarily decided on this cutoff for the number of variables and expressions, and wrote the code so this could be adjusted. By "high level" I mean not within a subexpression or exponent, or a function argument--so f(x + y) would not count as a substantive expression.

## A brief history of TeX

You might be wondering why tokenization and parsing  similar equations was hard enough a task to spend a whole semester doing it. You would be right to wonder: it should not be very hard to do, if not for the fact that the core layout algorithms for TeX are all written in a virtually extinct language called [WEB](https://en.wikipedia.org/wiki/WEB) written by the creator of TeX, Donald Knuth, himself. 

Because WEB has been all but forgotten, the core TeX algorithms implemented in it by Knuth are automatically cross-compiled into C code before being used by TeX tools like texlive. This makes it extremely difficult to hack into TeX's parsing algorithms and access their internal data structures. Without access to the TeX algorithms or internal data structures (or even source code that is easy to navigate and/or understand), it is hard to even tokenize LaTeX codes, not to mention parse them.

As a result, I have written my own tokenization function. I have not written a complete TeX parser, but I have implemented a shallow parse that can skip along the highest level of TeX code and check if it contains certain types of operations.

A group at Harvard wrote a wrapper around KaTeX for tokenizing LaTeX math expressions. I decided to write my own so that I could be absolutely certain about the assumptions underlying the data and avoid accidentally introducing bias into the data.

## Tokenization

I implemented a finite state machine to tokenize TeX codes. It takes a stream of characters from an equation from an arxiv text as input and iterates over it, changing state with each new character. Depending on the state and the character, the FSM will build a token or create a new one. 

The following input string will be tokenized to the following list by the function `tokenize` in `tok.py`:

`'\\frac{x} {y} \\begin{eq }x = \\textfadfsad{tets} \\int 1.0 .6 \\end{test}'` 

`['\\frac', '{', 'x', '}', '{', 'y', '}', '\\begin', '{', 'e', 'q', '}', 'x', '=', '\\text', 'fadfsad', '{', 't', 'e', 't', 's', '}', '\\int', '1.0', '.6', '\\end', '{', 't', 'e', 's', 't', '}']`


On the first pass, the tokenizer follows some extremely simple rules, like building every character a-z that comes after a \\ into a single token. This creates some incorrect tokens, like `\\intx`. So the tokenizer makes another pass along the now partially-tokenized expressions and attempts to break up any string starting with '\\' into a known macro. I acquired and merged two collections of known macros: 1 from CTAN (the official tex repository, you can check out the list in your browser at this link: [http://ctan.math.ca/tex-archive/info/symbols/comprehensive/SYMLIST](http://ctan.math.ca/tex-archive/info/symbols/comprehensive/SYMLIST)), and the other from KaTeX, Khan Academy's online math renderer. This function is called `fix_macros` and resides in `tok.py`

Example: 

`toks = tokenize('\\frac{x} {y} \\begin{eq }x = \\textfadfsad{tets} \\int 1.0 .6 \\end{test}')
fixed = fix_macros(toks, debug=True)
fixed == ['\\frac', '{', 'x', '}', '{', 'y', '}', '\\begin', '{', 'e', 'q', '}', 'x', '=', '\\text', 'fadfsad', '{', 't', 'e', 't', 's', '}', '\\int', '1.0', '.6', '\\end', '{', 't', 'e', 's', 't', '}']`

Location in codebase: `tok.py`. Tests in `test_tok.py`

You can run both of the commands together using the function `tokenize_and_fix_macros` in `tok.py`

## Further preparation

The following section goes over a series of functions I have written to further prepare the tokenized equations for a machine learning model. Keep in mind some, any, or all of these functions need not be used: You could modify them, write your own, or just use the output of the tokenization process for a model.

### Splitting

All code to do with splitting resides in `split.py`.

Splitting equations comes in two steps: 

1. Splitting equations that are in aligned environments, like the one below, into multiple expressions. These splits occur on:
* A "\\\\" (TeX for line break)
* A punction token (see all punctuation tokens in `data/punctuation_list.json`) that is not within a subexpression, A character is considered to be within a subexpression whenver it is within a two characters like "(" and ")" or "{" and "}". The full list of these characters comes from KaTeX's list of right and left bracket-type characters.
* A long inline text expression (long because we don't want to automatically split on something like `\\text{x}`) is encountered. 

Example of this first step:

One thing to note is that, if something like the following gets encountered, the bottom line gets "folded in" to the top one (this would be with a list of tokens in the code, I'm using TeX strings here for clarity).

`\begin{aligned} 
f(x) &= x + y^2 \\
     &= ax + b
\end{aligned}`

folding in =>

`f(x) = x + y^2 = ax + b`

The same rules apply to inline equations like `ax + b = 700x + z, ax + c = \theta + z`, which would be split into `ax + b = 700x + z` and `ax + c = \theta + z` (once again, these would actually be token lists in practice).

2. After expressions have been handled, equations are split on relations. I use a list of relations from KaTeX (`data/relation_list.json`) to find relations to split on. I only split when the relation is not within a left and right bracket-type character (like "{" and "}", see full list of right and left symbols in `open_list.json` and `close_list.json`). 

Example (stylized for clarity):

`f(x) + y = 100x^2` => `f(x) + y` and `100x^2`

(Actual example from the code)

`split(tokenize_and_fix_macros("5 = 6 \\\\ = 6 + 7"))`

Results in the following pairs:

`[[['5'], ['6'], ['6', '+', '7']]]`

Location in codebase: `split.py`. Tests in `test_split.py`


### Heuristics for finding useful pairs

Once we have tokenized and split our equations, we need to determine which of these expression pairs are worth keeping. One way to do this would be to just use a term-frequency-inverse-document-frequency (tf-idf) similarity score for each equation pair, setting some arbitrary cutoff.

#### TF-IDF
If you want to use tf-idf scores, you can with the data in `all_eqs` -- just read in the 'tokenized_equation_filtered' field from the json objects, rather than the 'aligned' field.

#### Other metrics

I wanted to use the parsing abilities I have developed to develop another sort of metric. In `suitable.py`, I have implemented a test that checks if a math expression has more than one variables/symbol/number and at least one operator (something like a plus sign). I use this as the metric to create the dataset in `all_eqs`.

As an example, this test would return True for the following (tokenized) expression: 

`['x', '+', '1.0', '900', '\\theta', '\\int']`

But If you removed the '+', it would return false.

Additionally, it will only count operators if they are on the "inside" of the expression, so that things like the following list of tokens don't count.

`['+', '1.0', '900', '\\theta', '\\int']`

Location in codebase: `suitable.py`. Tests in `test_suitable.py`

### Stoplisting

There are some tokens that add nothing to the mathematical meaning of the expression, such as `\begin{align}`. In addition, comments inside of `\text` tags, though perhaps pertaining to the equation, end up distracting from the meanining as well, since, to the model, any character inside the `\text` looks like a variable.

Sometimes people do just use `\text` tags to make a variable look a certain way: I wanted to keep as many of these as possible, so I struck a balance where I only excluded `\text` tags and their children (anything within {} brackets) when there were more than 4 tokens within the brackets ({}).

Example: 

The following expression: 

`filter_tokens(['\\int', '\\text', '{', 'x', '}', '\\text', '{', 'h', 'i', 't', 'h', 'e', 'r', 'e', '}', 'x', '+', 'y'])`

Results in:

`['\\int', '\\text', '{', 'x', '}', 'x', '+', 'y']`

The first text tag is kept since it is relatively harmless, surrounding a variable to make it look differently. The second text tag surrounds a fully fledged expression, and thus gets pruned.

Location in codebase: `filter_equations.py`. Tests in `test_filter_equations.py`

### Normalization

LaTeX allows you to write expressions like `\int_{x+y}^5` and `\int^5_{x+y}` and get equivalent representations. `^` and any of its dependents always come before `_` and its dependents. I considered implementing a function to normalize these types of expressions, but thinking about the state of the art in NLP modeling made me decide against it. When we tokenize a natural lanuage sentence like "The man was buying groceries and walking a dog", we don't worry about the fact that it is equivalent to "The man was walking a dog and buying groceries". Not needing to worry about this makes the models more flexible, easier to train (fewer pre-processing steps), and generally better, in my opinion.

# Some metrics

| Total Number of Equations | Useful Equation pairs identified | 
|---------------------------|----------------------------------| 
| 69,052,499                | 1,881,786                        | 


## TF-IDF similarity between identified pairs of equations versus random pairs

![Evaluating equation pairs via equivalencies](report/pairs_comparison.png "Evaluating equation pairs via equivalencies")

One way to evaluate how useful this process of splitting on relations is by checking the term-frequency-inverse-document-frequency similarity scores between the pairs of equations, and comparing these scores with randomly assigned pairs of equations. We would expect that equations identified via equivalencies would have a pretty high similarity to each other, on average, since people tend to repeat tokens on either side of a relation ($x + 6 = x + 3 + 3$, for example).

The histogram at the beginning of the section compares the similiarity scores for the two across a sample of 100,000 equations. A higher score on the x axis means equations are more similar. 

You can see, based on this graph, that the probability of a pair of equations identified through the methodology laid out in this report being similar is much higher than that of a random pair.

![Zooming in on the pairs](report/pairs_dist.png "Zooming in on the pairs")

It is a bit hard to see what the distribution of pairs identified through my methods is like since TF-IDF has such a higher peak. Plotted alone, the graph is more or less normally distributed. This is encouraging, since we would expect some sort of natural gradient to how similar equation are, and yet also expect many to be very similar (but not *too* similar).

# Technical details

Pre-processed equations are available in the folder `all_eqs`. If you want to run the processing job yourself, use the `pipeline.py` script. Just type something like `python pipeline.py -f eqs_100k.tsv -o test_pipeline_out` to start processing. Note: test_pipeline_out is a folder, not a file.


## A note on `all_eqs`

`all_eqs` contains files that have one json object per line. This allows easy read/write in a distributed environment. To read the equations in, you will need to open a file and then convert each line to json.

Within each json object, there are several fields: 

* 'aligned': the final output of the pipeline, a list of "interseting" looking equations that were related to each other by something like an equals sign (full list of relations used in `data/relations_list.json`).

* 'source_equation': the original equation tex(t)

* 'tokenized_equation': the equation after tokenization.

* 'rowid': the equation ID, corresponds with data from [The Hopper Project](https://github.com/hopper-project)

* 'tokenized_equation_filtered': The equation after being run through a stoplist of unuseful tokens (details under the filtering section in `report/report.md`)

## Notebooks

There are several notebooks that serve as examples/tutorials in this repository.

* `tf-idf benchmark.ipynb`: generates similarity measures between pairs of equations using term-frequency-inverse-document-frequency metrics.

* `katex data.ipynb`: explores data on latex macros and symbols from KaTeX's repository.

* `view_pairs.ipynb`: Showcases using ipython's built in `_repr_html_` methods to get a rich format for python objects in jupyter notebook cells.

## Testing

Type `pytest` from the root directory (`pip install pytest` if you don't have it).

## Development

If you'd like to adapt this for your own work, feel free. A good starting point would be looking through the test_* files for examples of what everything does.

### WARNING!!! MAKE SURE YOU ARE WORKING WITH UTF-8. OPEN THE FILE IN UTF-8. YOU WILL FAIL OTHERWISE.

## Improvements

Currently, it doesn't parse any sort of matrix or array alignment type, such as `array` or `pmatrix`. These are used surprisingly frequently to align equations.

nasty example:

\n\xymatrix@R=0.25cm @C=0.7cm{\nU \otimes (V \otimes W) \ar[r]^{c_{U,V \otimes W}}(V \otimes W) \otimes U \ar[dr]^{\alpha_{V,W,U}}\\\n(U \otimes V) \otimes W \ar[dr]_-{c_{U,V} \otimes W} \ar[ur]^{\alpha_{U,V,W}}V \otimes (W \otimes U)\\\n(V \otimes U) \otimes W \ar[r]_{\alpha_{V,U,W}}V \otimes (U \otimes W)\ar[ur]_{ V \otimes c_{U,W}}\n}\n

# Interesting examples

## Should we get rid of all text tags (like \mathcal)?

\bigcup_{i \in I} \Omega_i : {\mathcal{X}} {\dashrightarrow} {\mathcal{Y}},  \left( \bigcup_{i \in I} \Omega_i \right)(x):=
\bigcup_{i \in I} \Omega_i(x) \text{ for all } x \in {\mathcal{X}}.

# Things you may want to further filter:

"\\;" "\\,"

# Potential improvements:

Right now, \frac is considered an operator. This leads to a lot of akwardly short epressions like dx/dy making it into the final dataset however. This is more of a notation than an operation, so it might be worth writing a method to filter out such lone fractions. This would be easy to do by extending `filter_tokens.py`

# Sources of data for algorithms

First list of all mathematical symbols (from the TeX repository):

http://ctan.math.ca/tex-archive/info/symbols/comprehensive/SYMLIST

KaTeX:

https://github.com/Khan/KaTeX

Thank you to Khan Academy for building such a great tool!

# Bibliography

@inproceedings{schnabel_evaluation_2015,
	title = {Evaluation methods for unsupervised word embeddings},
	doi = {10.18653/v1/D15-1036},
	author = {Schnabel, Tobias and Labutov, Igor and Mimno, David and Joachims, Thorsten},
	month = jan,
	year = {2015},
	pages = {298--307}
}

@misc{samghelms_embeddings-viz:_2018,
	title = {embeddings-viz: demo of visualization tool {I}'ve been building using three.js and react},
	shorttitle = {embeddings-viz},
	howpublished = {https://github.com/samghelms/embeddings-viz},
	urldate = {2018-02-02},
	author = {Samuel Helms},
	month = jan,
	year = {2018},
	note = {original-date: 2018-01-19T22:18:35Z},
	file = {Snapshot:/Users/sam/Zotero/storage/JIIGW36U/embeddings-viz.html:text/html}
}

@misc{noauthor_react_nodate,
	title = {React {App}},
	howpublished = {http://ood.cs.uchicago.edu:5000/},
	urldate = {2018-02-02},
	author = {Samuel Helms},
	file = {React App:/Users/sam/Zotero/storage/DIKV4ZEN/ood.cs.uchicago.edu.html:text/html}
}

@misc{samghelms_mathviz:_2017,
	title = {mathviz: {A} python package for examining mathematics equation embeddings},
	copyright = {MIT},
	shorttitle = {mathviz},
	howpublished = {https://github.com/samghelms/mathviz},
	urldate = {2018-02-02},
	author = {Samuel Helms},
	month = dec,
	year = {2017},
	note = {original-date: 2017-11-01T23:40:18Z},
	file = {Snapshot:/Users/sam/Zotero/storage/H7V8QRUA/mathviz.html:text/html}
}

@article{mikolov_distributed_2013,
	title = {Distributed {Representations} of {Words} and {Phrases} and their {Compositionality}},
	url = {http://arxiv.org/abs/1310.4546},
	abstract = {The recently introduced continuous Skip-gram model is an efficient method for learning high-quality distributed vector representations that capture a large number of precise syntactic and semantic word relationships. In this paper we present several extensions that improve both the quality of the vectors and the training speed. By subsampling of the frequent words we obtain significant speedup and also learn more regular word representations. We also describe a simple alternative to the hierarchical softmax called negative sampling. An inherent limitation of word representations is their indifference to word order and their inability to represent idiomatic phrases. For example, the meanings of "Canada" and "Air" cannot be easily combined to obtain "Air Canada". Motivated by this example, we present a simple method for finding phrases in text, and show that learning good vector representations for millions of phrases is possible.},
	urldate = {2018-02-02},
	journal = {arXiv:1310.4546 [cs, stat]},
	author = {Mikolov, Tomas and Sutskever, Ilya and Chen, Kai and Corrado, Greg and Dean, Jeffrey},
	month = oct,
	year = {2013},
	note = {arXiv: 1310.4546},
	keywords = {Computer Science - Computation and Language, Statistics - Machine Learning, Computer Science - Learning},
	file = {arXiv\:1310.4546 PDF:/Users/sam/Zotero/storage/5KQL66IR/Mikolov et al. - 2013 - Distributed Representations of Words and Phrases a.pdf:application/pdf;arXiv.org Snapshot:/Users/sam/Zotero/storage/XSGEN36P/1310.html:text/html}
}

@inproceedings{pennington_glove:_2014,
	title = {Glove: {Global} {Vectors} for {Word} {Representation}},
	booktitle = {{EMNLP}},
	author = {Pennington, Jeffrey and Socher, Richard and Manning, Christopher D.},
	year = {2014}
}

@inproceedings{ramos_using_2003,
	title = {Using {TF}-{IDF} to {Determine} {Word} {Relevance} in {Document} {Queries}},
	author = {Ramos, Juan David Hincapié},
	year = {2003}
}

@misc{noauthor_neural_nodate,
	title = {A {Neural} {Network} for {Machine} {Translation}, at {Production} {Scale}},
	url = {https://research.googleblog.com/2016/09/a-neural-network-for-machine.html},
	abstract = {Posted by Quoc V. Le \& Mike Schuster, Research Scientists, Google Brain Team   Ten years ago, we announced the launch of Google Translate , ...},
	language = {en},
	urldate = {2018-02-02},
	journal = {Research Blog},
	file = {Snapshot:/Users/sam/Zotero/storage/V42C9XR2/a-neural-network-for-machine.html:text/html}
}