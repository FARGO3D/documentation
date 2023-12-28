extensions = ['sphinx.ext.mathjax']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u"FARGO3D User Guide"
copyright = u'2014-2023, Pablo Benítez Llambay, Frédéric Masset & Contributors'
exclude_patterns = []

#See https://sphinx-themes.org/#theme-sphinx-rtd-theme
html_theme = 'sphinx_book_theme'
#pip install sphinx-book-theme

html_title = u"FARGO3D User Guide"
html_static_path = ['_static',]
html_last_updated_fmt = '%b %d, %Y'
html_use_index = False
htmlhelp_basename = 'FARGO3DUserGuidedoc'

# -- Options for LaTeX output --------------------------------------------------
latex_custom = r'''
\definecolor{warningBgColor}{RGB}{221,233,239}'''

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': latex_custom,
    'sphinxsetup': 'warningBgColor={RGB}{255,204,204}'
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'FARGO3DUserGuide.tex', u'FARGO3D',
   u'Pablo Benítez Llambay, Frédéric Masset and Contributors', 'manual'),
]

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'fargo3duserguide', u'FARGO3D',
     [u'Pablo Benítez Llambay, Frédéric Masset and Contributors'], 1)
]

# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'FARGO3DUserGuide', u'FARGO3D',
   u'Pablo Benítez Llambay, Frédéric Masset and Contributors', 'FARGO3DUserGuide', 'One line description of project.',
   'Miscellaneous'),
]