oshlex
======

**oshlex** (Object shlex) - Rule based unix-style config parser written
with shlex

This is a project made to simplify the task of reading and parsing
UNIX-style configuration files. It's simply an abstraction, using shlex
library, that provides an easy way to parse configuration files, by
creating a set of rules and handlers, which are then used to transform
tokens into python data structures.

**Warning**: At this moment only python >3.4 is supported, python2.7
support is planned in the near future.

Configuration syntax
~~~~~~~~~~~~~~~~~~~~

The configuration files syntax by default tries to follow the standard
UNIX configuration files syntax, as found in, for example nginx configs.
This is changed by simply subclassing Tokenizer class, or creating your
own class, that works identically to shlex.shlex class (Read `shlex
documentation <https://docs.python.org/3.4/library/shlex.html>`__ for
details)

Sample configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    server {
            host 127.0.0.1;
            port 10000;
            user {
                    username admin;
                    password admin;
            }
            user {
                    username test;
                    password test;
            }
    }

Usage
~~~~~

*oshlex.config* has two basic classes, **Rule** and **Configuration**.

*oshlex.handlers* has a couple of predefined handlers (text and integer)

Creating rules
^^^^^^^^^^^^^^

In this example we define some rules, to parse the example configuration
file, as shown above.

The basic idea is to create root rule and pass it to Configuration
object while initializing. Every other rule is therefore a subrule of
"root" rule.

The **Rule** class accepts following parameters:

*name* - The name of rule, defaults to "root"

*handler* - Handler function, that accepts the list of tokens and
outputs python data structure to be used in the application.
*oshlex.handlers* module has two predefined handler functions - *text*,
which accepts a list of tokens and returns the first one as a string, or
raises an UnacceptableTokenCount exception, if list of tokens contains
more than one element, and *integer*, which does basically the same
thing, only returns python *int* object, or raises *UnacceptableToken*
exception if token is not convertable to the *int* type. defaults to
*None*, which means that the token is represented by python dictionary
with subtokens.

*unique* - bool, defines if it is acceptable or not for said option to
be defined in the config file more than one once. If *True*, raises a
ConfigError exception if option is defined in two places at the same
time. If *False*, appends every occurence of the option definition to
the list. Defaults to *False*

*mandatory* - bool, pretty self-explanatory, if option is mandatory, but
not defined - raises *MandatoryOptionMissing* exception, otherwise does
nothing.

Basic example
^^^^^^^^^^^^^

.. code:: python

    from oshlex.config import Rule, Configuration
    from oshlex import handlers

    # Defining rules
    root = Rule('root')
    server = Rule('server', unique=True, mandatory=True)
    host = Rule('host', handler=handlers.text, unique=True, mandatory=True)
    port = Rule('port', handler=handlers.integer, unique=True, mandatory=True)
    user = Rule('user', unique=False, mandatory=False)
    username = Rule('username', handler=handlers.text, unique=True, mandatory=True)
    password = Rule('password', handler=handlers.text, unique=True, mandatory=True)

    # Chaining rules together
    user.add(username)
    user.add(password)
    server.add(host)
    server.add(port)
    server.add(user)
    root.add(server)

    conf = Configuration(root, './example.conf')
    conf.read()

This way we get the Configuration object (conf) with following
structure:

.. code:: python

    {
      'server': {
        'host': '127.0.0.1',
        'port': 10000,
        'user': [
          {'password': 'admin', 'username': 'admin'},
          {'password': 'test', 'username': 'test'}
        ]
    }}

Configuration object is subscriptable, so everything you can do with
dictionaries is allowed here:

.. code:: python

    >>> conf['server']['host']
    '127.0.0.1'

You can define your own handlers, which are just functions that accept a
list of tokens and return something that python can work with, if you
need to parse given tokens in some other ways, for example, we have an
option that accepts ranges (e.g 1-10), we then need to define a hadler
to convert these ranges into lists of integers, so we write a handler:

.. code:: python

    from oshlex.handlers import UnacceptableToken, UnacceptableTokenCount
    def range(tokens):
        if len(tokens) > 1:
            raise UnacceptableTokenCount('This handler accepts 1 token at most')

        try:
            start, end = [int(token) for token in tokens[0].split('-')]
        except Exception as e:
            raise UnacceptableToken('Couldn\'t process token {}, got {}'.format(tokens[0], e))

        return [i for i in range(start, end)]                                                                                   
