========
qualname
========

Python module to emulate the ``__qualname__`` attribute for classes and methods
(Python 3.3+) in older Python versions. See `PEP 3155`__ for details.

__ https://www.python.org/dev/peps/pep-3155/

Installation
============

::

  pip install qualname


Usage
=====

Assume these definitions:

::

  class C:
      def f():
          pass

      class D:
          def g():
              pass

In Python 3.3+, classes have a ``__qualname__`` property::

  >>> C.__qualname__
  'C'
  >>> C.f.__qualname__
  'C.f'
  >>> C.D.__qualname__
  'C.D'
  >>> C.D.g.__qualname__
  'C.D.g'

Unfortunately, Python 2 and early Python 3 versions do not have an (obvious)
equivalent. ``qualname`` to the rescue::

  from qualname import qualname

  >>> qualname(C)
  'C'
  >>> qualname(C.f)
  'C.f'
  >>> qualname(C.D)
  'C.D'
  >>> qualname(C.D.g)
  'C.D.g'

Victory!


How does it work?
=================

Glad you ask.

This module uses source code inspection to figure out how (nested) classes and
functions are defined in order to determine the qualified name for it. That
means parsing the source file, and traversing the AST (abstract syntax tree).
This sounds very hacky, and it is, but the Python interpreter itself does not
have the necessary information, so this justifies extreme measures.

Now that you know how it works, you'll also understand that this module only
works when the source file is available. Fortunately this is the case in most
circumstances.


License
=======

BSD.


Feedback? Issues?
=================

https://github.com/wbolster/qualname
