# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
from recommonmark.parser import CommonMarkParser
project = 'wiki.slank.dev'
copyright = '2019, slankdev'
author = 'slankdev'
release = '0.0.0'
master_doc = 'index'
source_suffix = ['.rst','.md']
source_parsers = { '.md': CommonMarkParser, }
extensions = [ ]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

# -- Options for HTML output -------------------------------------------------
html_logo = '_static/slankdev.png'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

def setup(app):
  app.add_css_file('custom.css')
