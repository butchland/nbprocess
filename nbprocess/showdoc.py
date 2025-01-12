# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/08_showdoc.ipynb.

# %% auto 0
__all__ = ['get_name', 'qual_name', 'ShowDocRenderer', 'BasicMarkdownRenderer', 'show_doc', 'BasicHtmlRenderer', 'showdoc_nm']

# %% ../nbs/08_showdoc.ipynb 3
from fastcore.docments import *
from fastcore.utils import *
from importlib import import_module
from .doclinks import *
import inspect

from .read import get_config

# %% ../nbs/08_showdoc.ipynb 4
def get_name(obj):
    "Get the name of `obj`"
    if hasattr(obj, '__name__'):       return obj.__name__
    elif getattr(obj, '_name', False): return obj._name
    elif hasattr(obj,'__origin__'):    return str(obj.__origin__).split('.')[-1] #for types
    elif type(obj)==property:          return _get_property_name(obj)
    else:                              return str(obj).split('.')[-1]

# %% ../nbs/08_showdoc.ipynb 5
def qual_name(obj):
    "Get the qualified name of `obj`"
    if hasattr(obj,'__qualname__'): return obj.__qualname__
    if inspect.ismethod(obj):       return f"{get_name(obj.__self__)}.{get_name(fn)}"
    return get_name(obj)

# %% ../nbs/08_showdoc.ipynb 6
class ShowDocRenderer:
    def __init__(self, sym, disp:bool=True):
        "Show documentation for `sym`"
        store_attr()
        self.nm = qual_name(sym)
        self.isfunc = inspect.isfunction(sym)
        self.sig = inspect.signature(sym)
        self.docs = docstring(sym)

# %% ../nbs/08_showdoc.ipynb 7
class BasicMarkdownRenderer(ShowDocRenderer):
    def _repr_markdown_(self):
        doc = '---\n\n'
        if self.isfunc: doc += '#'
        doc += f'### {self.nm}\n\n> **`{self.nm}`**` {self.sig}`'
        if self.docs: doc += f"\n\n{self.docs}"
        return doc

# %% ../nbs/08_showdoc.ipynb 8
def show_doc(sym, disp=True, renderer=None):
    if renderer is None: renderer = get_config().get('renderer', None)
    if renderer is None: renderer=BasicMarkdownRenderer
    elif isinstance(renderer,str):
        p,m = renderer.rsplit('.', 1)
        renderer = getattr(import_module(p), m)
    return renderer(sym or show_doc, disp=disp)

# %% ../nbs/08_showdoc.ipynb 13
class BasicHtmlRenderer(ShowDocRenderer):
    def _repr_html_(self):
        doc = '<hr/>\n'
        lvl = 4 if self.isfunc else 3
        doc += f'<h{lvl}>{self.nm}</h{lvl}>\n<blockquote><code>{self.nm}{self.sig}</code></blockquote>'
        if self.docs: doc += f"<p>{self.docs}</p>"
        return doc

# %% ../nbs/08_showdoc.ipynb 15
def showdoc_nm(tree):
    "Get the fully qualified name for showdoc."
    return ifnone(get_patch_name(tree), tree.name)
