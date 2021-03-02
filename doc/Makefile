# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
SPHINXDOC     = sphinx-apidoc

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

rst:
	@$(SPHINXDOC)  --ext-autodoc --ext-coverage --ext-viewcode \
	 -P -F -T -l -f -o "$(SOURCEDIR)"/code \
	../ ../framework/dataspace/tests \
	../framework/util/tests ../framework/engine/tests
	rm -f source/code/setup.rst
clean:
	@rm -rf "$(SOURCEDIR)"/code "$(BUILDDIR)"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
