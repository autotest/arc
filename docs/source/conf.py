# -*- coding: utf-8 -*-

import sys
import os
import arc.version

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.todo',
              'sphinx.ext.coverage']

# local definitions reused throught the configuration
_SHORTNAME = u'arc'
_AUTHOR = u'Cleber Rosa'
_TITLE = u'arc Documentation'
_COPYRIGHT = u'2012-2013, Red Hat, Inc.'

master_doc = 'index'
project = u'Arc'
copyright = _COPYRIGHT
version = '%s.%s' % (arc.version.MAJOR, arc.version.MINOR)
release = arc.version.VERSION

latex_documents = [
    ('index', 'arc.tex', _TITLE,
     _AUTHOR, 'manual'),
]

texinfo_documents = [
    ('index', 'arc', _TITLE,
     _AUTHOR, 'arc', 'Autotest RPC Client',
     'Miscellaneous'),
]

epub_title = _SHORTNAME
epub_author = _AUTHOR
epub_publisher = _AUTHOR
epub_copyright = _COPYRIGHT

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}
