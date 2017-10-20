---
title: ilabs.client
---
# ilabs.client
[![Build Status](https://travis-ci.org/innodatalabs/ilabs.client.svg?branch=master)](https://travis-ci.org/innodatalabs/ilabs.client)
[![PyPI version](https://badge.fury.io/py/ilabs.client.svg)](https://badge.fury.io/py/ilabs.client)


Python client to access api.innodatalabs.com endpoints.

## Building

```
virtualenv .venv -p python3  # or python2, as appropriate
. .venv/bin/activate
pip install -r requirements.txt
pip install mock nose

nosetests ilabs/client/test
```

## Usage

There are three levels of API access:

  * low level, implemented by `ilabs.client.ilabs_api.ILabsApi` class. It
    pretty much mirrors the REST endpoints as documented on [InnodataLabs
    website](http://developer.innodatalabs.com).
  * intermediate level, implemented by
    `ilabs.client.ilabs_predictor.ILabsPredctor` class. This class can
    be used to do a file-in => file-out prediction. Most (but not all)
    InnodataLabs endpoints provide this type of prediction.
  * high level, implemented by `ilabs.client.ilabs_tagger.ILabsTagger` class,
    This one is specialized for doing dense sequence labeling.

### ILabsApi
Low-level access to the InnodataLabs API endpoints. Takes care of the
following concerns:

1. Looks up user authentication key, if not provided explicitly.
2. Modifies request headers to include user authentication key

Example:
```
api = ILabsApi(user_key='1234567890')  # use the real key here, please!
api.ping()
```

### ILabsPredictor
Implements file-in to file-out process. Takes care of polling for the
asynchronous job status.

Example:
```
predictor = ILabsPredictor.init(
    domain='ilabs.bib',
    user_key='0123456789')  # use the real key, please!

binary_data = b'''<brs:b xmlns:brs="http://innodatalabs.com">
<brs:r>Jack Nadeau and Mike Abukhoff, Continuous Machine Learning, \
Innodata Press, Noida, India</brs:r>
<brs:r>Bill Gates, Microsoft Kills Windows, Finally!, \
Private communication, 2019</brs:r>
</brs:b>
'''

predicted_tagging = predictor(binary_data, progress=print)

// this will return serialized XML file with predicted tagging
```

## ILabsTagger
High-level class that simplifies calling endpoints that do dense sequence
labeling. For this kind of tasks input is a string, and output is the tagging
for this string. For efficiency, API operates on a batch of strings, and
returns parallel list of predicted annotations.

Example:
```
predictor = ILabsTagger(
    domain='ilabs.bib',
    user_key='0123456789')  # use the real key, please!

records = [
    'Jack Nadeau and Mike Abukhoff, Continuous Machine Learning, Innodata Press, Noida, India',
    'Bill Gates, Microsoft Kills Windows, Finally!, Private communication, 2019'
]
predicted_tagging = predictor(records, progress=print)

assert len(predicted_tagging) == len(records)
assert predicted_tagging[0] == [
  ('', None)
]
```
