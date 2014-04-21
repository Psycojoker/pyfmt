Introduction
============

Pyfmt is an autoformatting source code tool for python, in more or less the
same spirit than [gofmt](http://golang.org/cmd/gofmt/). It follows the pep8 and
uses [Baron](https://github.com/Psycojoker/baron) to do its work in one pass.

**Pyfmt is in its early stage of developpement, it already do a good job at
formatting most of python code but it doesn't handle yet splitting a too long
line and might end up putting back into one line a line that you have split.**
But it should be fine for ~80% of the cases.

Feedback is very welcome.

Installation
============

    pip install git+https://github.com/Psycojoker/pyfmt.git

Usage
=====

    pyfmt file.py  # output to standard output
    pyfmt -i file.py  # replace the content of the file, like -i of sed

From python:

```python
from pyfmt import format_code

format_code(source_code)
```

Community
=========

You can reach us on [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)
