# Intro

This repository contains work I have done for my senior thesis to identify similar equations written in latex.

You can read more about the specifics of the project in writeup.md, or by downloading the pdf ({INS_LINK}).

Pre-processed equations are available in the folder `all_eqs`. If you want to run the processing job yourself, use the `pipeline.py` script. Just type something like `python pipeline.py -f eqs_100k.tsv -o test_pipeline_out` to start processing. Note: test_pipeline_out is a folder, not a file.

# A note on `all_eqs`

`all_eqs` contains files that have one json object per line. This allows easy read/write in a distributed environment. To read the equations in, you will need to open a file and then convert each line to json.

Within each json object, there are several fields: 

* 'aligned': the final output of the pipeline, a list of "interseting" looking equations that were related to each other by something like an equals sign (full list of relations used in `data/relations_list.json`).

* 'source_equation': the original equation tex(t)

* 'tokenized_equation': the equation after tokenization.

* 'rowid': the equation ID, corresponds with data from [The Hopper Project](https://github.com/hopper-project)

* 'tokenized_equation_filtered': The equation after being run through a stoplist of unuseful tokens (details under the filtering section in `report/report.md`)

# Notebooks

There are several notebooks that serve as examples/tutorials in this repository.

* `tf-idf benchmark.ipynb`: generates similarity measures between pairs of equations using term-frequency-inverse-document-frequency metrics.

* `katex data.ipynb`: explores data on latex macros and symbols from KaTeX's repository.

* `view_pairs.ipynb`: Showcases using ipython's built in `_repr_html_` methods to get a rich format for python objects in jupyter notebook cells.

* 

# Testing

Type `pytest` from the root directory (`pip install pytest` if you don't have it).

# Development

If you'd like to adapt this for your own work, feel free. A good starting point would be looking through the test_* files for examples of what everything does.

# WARNING!!! MAKE SURE YOU ARE WORKING WITH UTF-8. OPEN THE FILE IN UTF-8. YOU WILL FAIL OTHERWISE.

# Improvements

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
