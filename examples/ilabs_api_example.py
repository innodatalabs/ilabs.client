# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
from ilabs.client.ilabs_api import ILabsApi

api = ILabsApi()  # uses indirect authentication
out = api.ping()
print('ping:', out)

bibliography_brs = '''<brs:b xmlns:brs="http://innodatalabs.com/brs">

<brs:r>Lucas Theis, Aäron van den Oord, and Matthias Bethge. A note on the \
evaluation of generative models. ICLR, 2016.</brs:r>

<brs:r>Luc Devroye. Sample-based non-uniform random variate generation. \
Springer-Verlag, New York, 1986.</brs:r>

</brs:b>
'''.encode('utf-8')

out = api.upload_input(bibliography_brs)
print('upload_input:', out)

input_filename = out['input_filename']

out = api.download_input(input_filename)
print('download_input:', out)
assert out == bibliography_brs

out = api.predict('ilabs.bib', input_filename)
print('predict:', out)
task_id = out['task_id']
document_output_url = out['document_output_url']

import time

for _ in range(10):
    print('Waiting for asynchronous job to complete...')
    time.sleep(1)

    out = api.status('ilabs.bib', task_id)
    print('status:', out)
    if out['completed']:
        break
else:
    assert False, 'Timeout'

assert out.get('error') is None, out

out = api.get(document_output_url)
print('get:', out)

bibliography_expected_output = '''<?xml version='1.0' encoding='utf-8'?>
<brs:b xmlns:brs="http://innodatalabs.com/brs">\

<brs:r c="4.76"><brs:s l="author-person">Lucas Theis</brs:s>, <brs:s l="author-person">Aäron van den Oord</brs:s>, and <brs:s l="author-person">Matthias Bethge</brs:s>. <
brs:s l="titletext">A note on the evaluation of generative models</brs:s>. <brs:s l="sourcetitle">ICLR</brs:s>, <brs:s l="publicationyear">2016</brs:s>.</brs:r>\

<brs:r c="2.41"><brs:s l="author-person">Luc Devroye</brs:s>. <brs:s l="sourcetitle">Sample-based non-uniform random variate generation</brs:s>. Springer-Verlag, New York
, <brs:s l="publicationyear">1986</brs:s>.</brs:r>\

</brs:b>'''.encode('utf-8')

bibliography_expected_output = b'''<?xml version='1.0' encoding='utf-8'?>
<brs:b xmlns:brs="http://innodatalabs.com/brs">
<brs:r c="4.76"><brs:s l="author-person">Lucas Theis</brs:s>, <brs:s l="author-person">A\xc3\xa4ron van den Oord</brs:s>, and <brs:s l="author-person">Matthias Bethge</brs:s>. <brs:s l="titletext">A note on the evaluation of generative models</brs:s>. <brs:s l="sourcetitle">ICLR</brs:s>, <brs:s l="publicationyear">2016</brs:s>.</brs:r>
<brs:r c="2.41"><brs:s l="author-person">Luc Devroye</brs:s>. <brs:s l="sourcetitle">Sample-based non-uniform random variate generation</brs:s>. Springer-Verlag, New York, <brs:s l="publicationyear">1986</brs:s>.</brs:r>
</brs:b>'''
assert out == bibliography_expected_output

out = api.upload_feedback('ilabs.bib', '000000-000000-0000-00000000.html', bibliography_expected_output)
print('upload_feedback', out)