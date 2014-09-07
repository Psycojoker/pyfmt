PyFmt
======

`Pyfmt` is an autoformatting source code tool for `python`, in more or less the
same spirit than [gofmt](http://golang.org/cmd/gofmt/). It follows the `pep8` and
uses [Baron](https://github.com/Psycojoker/baron) to do its work in one pass.

**`Pyfmt` is in its early stage of developpement, it already do a good job at
formatting most of python code but it doesn't handle yet splitting a too long
line and might end up putting back into one line a line that you have split.**
But it should be fine for ~80% of the cases.

Feedback is very welcome.

You can see it in action [here](https://github.com/Psycojoker/pyfmt/commit/145a186b00f842d62be71959f698f84b033310ff).

Installation
============
`PyFmt` can be installed using `$ pip install pyfmt`

Usage
=====

    pyfmt file.py  # output to standard output
    pyfmt -i file.py  # replace the content of the file, like -i of sed

From `python`:

```python
from pyfmt import format_code

format_code(source_code)
```

Community
=========

You can reach us on [irc.freenode.net#baron](https://webchat.freenode.net/?channels=%23baron)

Tests
=====
You can run the tests using `$ py.test test_pyfmt.py`

Operations
==========

Things that `pyfmt` do (if it's not already done in the code):

* render ALL nodes of the python language according to the `pep8`
* if a datastructure is indented, keep the indentation and indent it according to the pep8
* put 2 spaces before comments after code, put a space after the "#" of the comment (don't do for shebang)
* split compound statements written on one line on two lines (example: `if a: pass` -> `if a:\n`    pass", same for every other statements that wait for a block of code)
* replace `stuff` by repr(stuff)
* split multiple import across multiple lines
* replace tabs with space
* correctly indent the whole file using 4 spaces
* convert windows `'\r\n`' to `'\n'`
* if not present, put two blank lines around functions or class definitions at the root level of the file
* if not present, put one blank line around method definition in a class
* replace <code><></code> with !=

Things that `pyfmt` don't do or don't do yet and that can be annoying:

* properly formatting the content of a "from x import (lot of stuff)"
* properly splitting too long lines, it may ends up putting back on one line a splited line
* removing extra blank lines
