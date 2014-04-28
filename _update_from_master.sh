#!/bin/sh
git checkout master -- output downloads
rm -rf html
mv output/html/* .
git add html
git rm -rfq output
git add html *.html *.xml *.png
git show master:bolttools/doc/blt_spec_dev.rst | rst2html --template _spec_template.txt > doc/general/specification_dev.html
#cp bolttools/doc/processing.* doc/general
#git add doc/general/processing.* doc/general/specification.html
