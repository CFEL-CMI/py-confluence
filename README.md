# py-confluence

CFEL Controlled Molecule Imaging tools for Atlassian Confluence.

This packages provides a few scripts to help using Confluence in a systematic
fashion; see description of the individual files below.

This package is provided as is and without any warranty included! If you have
improvements or further tools, please send a patch to the maintainer (see
setup.py) so we can include it in the distribution.

For installation, follow the standard Python approach, i.e., run
```
python setup.py install --user
```
in the top-level directory of the project.


## confluence_create-CMI-space

Creates a space according to the standard CMI layout.


## confluence_clone-space

Create a local html/xml copy of a the latest/current version of a complete
space; all content is put into a git repository to allow for versioning of the
downloaded content.


<!-- Put Emacs local variables into HTML comment
Local Variables:
coding: utf-8
fill-column: 80
End:
-->
