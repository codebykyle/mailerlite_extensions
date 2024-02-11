mailerlite_extensions
==========================

[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)

## Mailerlite Extensions
This package extends the Mailerlite Python library to include useful features like a cached group model which
limits round trips to Mailerlite, and additional subscriber functions left out of the official package like
updating a users e-mail address.

## Installing

`pip install git+https://github.com/codebykyle/mailerlite_extensions/tree/master`

or via ssh:

`pip install git+ssh://git@github.com/codebykyle/mailerlite_extensions.git`

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

## Todo

- Add unit tests
