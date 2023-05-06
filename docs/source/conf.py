import sys
import os

sys.path.append(os.path.abspath('D:/PythonWeb/HW/PWHomeWork14/'))

project = 'Contacts Rest API'
copyright = '2023, Ursus'
author = 'Ursus'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
