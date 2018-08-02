# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
from ilabs.client.ilabs_datavault_api import ILabsDatavaultApi
import logging
import contextlib

logging.basicConfig(level=logging.DEBUG)

@contextlib.contextmanager
def show_err():
    try:
        yield
    except Exception as err:
        print(err);
        print('Message:', err.read())
        raise

api = ILabsDatavaultApi()  # uses indirect authentication

NAME = 'redtag'


out = api.ping()
print('ping:', out)


num_collections = api.count_collections()
print('Number of existing collections:', num_collections)

collections = api.list_collections()
print('Existing collections:')
for collection in sorted(collections):
    print('\t', collection)

if NAME not in collections:
    api.create_collection(NAME)

policy = api.get_collection_policy(NAME)
print('Policy:', policy)

api.set_collection_policy(NAME, {
        'owner': NAME,
        'grants': {'api.innodatalabs.com': ['write']},
        'license': None
})

api.upload(b'Hello, world!', NAME, 'test-document.txt')
api.upload(b'Bye, world!', NAME, 'test-document.txt', facet='output')

num_docs = api.count_documents(NAME)
print('Number of documents:', num_docs)

documents = api.list_documents(NAME)
print('Documents:')
for doc in documents:
    print('\t', doc)

binary_data = api.download(NAME, 'test-document.txt', facet='output')
assert binary_data == b'Bye, world!'

facets = api.list_facets(NAME, 'test-document.txt')
print('Facets:')
for facet in facets:
    print('\t', facet)

num_facets = api.count_facets(NAME, 'test-document.txt')
print('Number of facets for this document:', num_facets)
