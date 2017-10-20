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

Quick start examples: http://github.com/innodatalabs/ilabs.client/examples

User guide and API reference: https://innodatalabs.github.io/ilabs.client
