# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
from ilabs.client.ilabs_tagger import ILabsTagger

tagger = ILabsTagger(domain='ilabs.bib')
out = tagger.predictor.api.ping()
print('ping:', out)

bibliography_records = [
    'Lucas Theis, Aäron van den Oord, and Matthias Bethge. A note on the \
evaluation of generative models. ICLR, 2016.',

    'Luc Devroye. Sample-based non-uniform random variate generation. \
Springer-Verlag, New York, 1986.'
]

out = tagger(bibliography_records, progress=print)
for ann in out:
    print(ann)
