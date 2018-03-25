from IPython.display import (display_javascript, display_html)
from uuid import uuid1
import json


class katex(object):
    def __init__(self, s):
        self._s = json.dumps(s)
        self.dep = "katex"
        self._ids = []
        self._katex = ("var katex_try = function(s, el) {\n"
                       "\t try {"
                       "\t\twindow.katex.render(s, el);\n"
                       "} catch(err) {\n"
                       "\t\t el.innerHTML = s;\n"
                       "\t}\n}")
        self._ctx = lambda body: "\nvar ctx = function()\
                                  {\n"+body+"\n}\nctx();\n"
        self._whenavailable_func = ("var whenAvailable = function(name,\
                                     callback) {\n"
                                    "\tvar interval = 10; // ms\n"
                                    "\twindow.setTimeout(function() {\n"
                                    "\tif (window[name]) {\n"
                                    "\t\tcallback();\n"
                                    "\t} else {\n"
                                    "\t\twindow.setTimeout(arguments.callee,\
                                     interval);\n"
                                    "\t}\n"
                                    "}, interval);\n"
                                    "}\n")
        _parent = 'var parent = document.getElementById(id);'
        _body = lambda math: "\n".join(["var newChild = document.createElement('span');",
                                        'katex_try({math}, newChild);'.format(math=math),
                                        "parent.appendChild(newChild);"])
        self._fn = lambda math: "var render_katex = function(id) { \n\t"+_parent+"\n\t"+_body(math)+"\n}"
        self._exec = lambda uid: 'whenAvailable("katex", function(){render_katex("'+uid+'");});'
#         self._exec = lambda uid: 'render_katex("'+uid+'");'
        self._filled_ctx = lambda uid, math: self._ctx("\n".join([self._whenavailable_func, self._katex,
                                                                  self._fn(math), self._exec(uid)]))

    def _repr_html_(self):
        unique_id = str(uuid1())
        anchor = '<div id="{unique_id}"/>'.format(unique_id=unique_id)
        self._ids.append(unique_id)
        return anchor

    def _repr_javascript_(self):
        js = []
        while len(self._ids) > 0:
            i = self._ids.pop(0)
            funcs = self._filled_ctx(i, self._s)
            js.append(funcs)
        return "\n".join(js)

    def _ipython_display_(self):
        display_html(self._repr_html_(), raw=True)
        display_javascript(self._repr_javascript_(), raw=True)
