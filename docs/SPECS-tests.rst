=============================================================
Improvised Data-Driven Multi-Language Test (iDMT) File Format
=============================================================

----------
Test Files
----------
The iDMT is a declarative system which describes tests by an initial
state, the name of a function, inputs to the function and the outcome.
Each test under this system tests only one function and one set of
inputs.

Testing data are contained in one or more JSON files. The format of
a JSON file is specified in ECMA-404.

-------------------
Filename Convention
-------------------
Each test file is named after the class (or module for non-OOP
platforms) that is being tested. For example, if there is a class or
module named ``TestSub``, all files beginning with ``TestSub`` and
ending with ``.json`` will make up the complete test suite.

An example test suite's list of files could look like the following:

::

    TestSub.json
    TestSub-extended.json
    TestSub-errors-2.json

Names are case-sensitive.

------
Format
------
Test specifications are written as JSON objects as follows:

Test File overview
==================

::

    {
        "name": TEST_SUITE_NAME,
        "tests": TESTS
    }

``TEST_SUITE_NAME`` is a string

TESTS
=====

::

    {
        TEST_0: TEST_SPEC,
        ...
        TEST_n: TEST_SPEC,
    }

TEST_SPEC
=========

::

    {
        TEST_NAME: {
            "fn_name": FUNCTION_NAME,
            "init": OBJECT_INIT_STATE,
            "out": EXPECTED_OUTPUT,
            "error": EXPECTED_EXCEPTION
        }
    }

``FUNCTION_NAME`` is a string naming the function being tested.
The name is case-sensitive on most platforms.

``EXPECTED_OUTPUT`` is the output of the function, as encoded as a
JSON object.

OBJECT_INIT_STATE
=================
On OOP platforms this is a representation of the test object's initial
state. For non-OOP platforms, it is a list of variables to be set.

For example, in a test file named ``HiClass.json``:

::

   { "init": { "name": "dave", "member": 1 } }

On OOP plaftorms with named arguments, it represents an object that
could be created with the constructor call:

::

    HiClass(name='dave', member=1)

When there is no support for named arguments, the values must be
passed in order of appearance:

::

    HiClass('dave', 1)

On non-OOP plaftorms it is equivalent to the following pseudocode:

::

    let name:str = "dave"
    let member:int = 1

If ``init`` is omitted, no object or variable will be created or set.

EXPECTED_EXCEPTION
==================
String representing the type of exception expected.

Supported options are: ``"any"``, ``"arithmetic"``, ``"index"``,
``"key"``, ``"type"`` and ``"value"``.

  TODO: Currently ``out`` cannot be used with ``exception``, yet there
  is a potential use case for simultaneous ``out`` and ``exception``.
  When used with ``exception``, ``out`` could represent details of an
  Exception (e.g. error codes and messages).
