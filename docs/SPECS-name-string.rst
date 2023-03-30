========================
PersonalName Name String
========================
Version 1.23.2

----------------------
Prerequisite Knowledge
----------------------
This specification assumes a reasonable understanding of the concept
and specifications of Configuration Strings (``config_str``). Details
of Configuration Strings are also found in the Technical
Documentation.

------
Syntax
------
A Name String (``name_str``) is a Unicode string of the following syntax:

::

   MAIN_NAME (ALT_NAME_1, ..., ALT_NAME_N)

``MAIN_NAME`` is made of zero or more elements; the ``ALT_NAME``
elements are alternate names, treated as a single element each,
appearing in a list between an opening and closing delimiter.

``ALT_NAME`` elements are optional, and the alternate name list is
optional.

Name strings should be accompanied by, or reference a configuration
string to assign a method of interpreting the name.

Configuration Strings may be embedded:

::

   MAIN_NAME (ALT_NAME_1, ..., ALT_NAME_N); CONFIG_STR

Configuration strings may be referenced, like in this table database
example:

::

    Name                                     Config
    =======================================  ===========
    MAIN_NAME (ALT_NAME_1, ..., ALT_NAME_N)  CONFIG_NAME


    Config_Name            Config_String
    =====================  =============
    CONFIG_NAME            CONFIG_STR

Exact methods of bundling name and configuration strings are currently
deemed to be application-specific and thus not covered by this
specification.

Spaces in Main Name Elements
============================
Space substitutes must be used in place of spaces that appear *within*
an element of the main name. These are converted back to spaces in
presentation-ready form.

Examples:

* ``Muhammad ibn Abu_Bakr`` ("Abu Bakr" is a single element)

* ``Wu Ze_Tian`` ("Ze Tian" is a single element)

The default space substitute is the underscore (U+005F), which may be
overridden by setting ``MNSU`` in the config_str.

Default Separator Characters
============================
By default:

* Main name elements are separated by ASCII spaces (U+0020)

* Alternate names are separated by ASCII commas (U+002C)

* The list of alternate names appear after the first left-facing
  round parenthesis (U+0028) and the last right-facing parenthesis
  (U+0029).

Default separator characters can be overridden using the following
configuration options:

* ``ALET``: Alternate name list end

* ``ALST``: Alternate name list start

* ``ALSE``: Alternate name list seperator

* ``MNSP``: Main Name inter-element space/separator

-------------------------
Element Types and Indexes
-------------------------
Main name elements may be assigned element types by assigning the
types by the element's index in ``config_str``.

Indexes
=======
In the example main name ``Muhammad ibn Abu_Bakr al-Khwarizmi``:

* There are four elements with their indexes:

  * Muhammad (index: 1)

  * ibn (2)

  * Abu Bakr (3)

  * al-Khwarizmi (4)

* Negative indexes may be used for addressing elements relative to
  the end of the name:

  * -1: al-Khwarizmi

  * -2: Abu Bakr

  * -3: ibn

  * -4: Muhammad

* Element types can be used as indexes if main name elements have
  been assigned a type. Given a ``config_str`` of

  ``N1=1;FD=2;F1=3;NS=4``

  * ``N1`` resolves to 1 (Muhammad)

  * ``FD`` resolves to 2 (ibn)

  * ``F1`` resolves to 3 (Abu Bakr)

  * ``NS`` resolves to 4 (al-Khwarizmi)

Please note that the zero index is only for use as an "element not
present" value in non-objective programming languages that lack a
global Null object.

Each marker or index may only be used once.

All main name elements should have an assigned element type.

Invalid Indexes
---------------
A positive index that refers to an element past the end of the name
resolves to an empty string.

Resolving a zero or unsuported index is an error.

Main Name Element Types
=======================
The following element types are supported:

1.  N1: First Name

2.  NM: Middle Name

3.  NS: Surname

4.  F1: First Parent or Father's First Name

5.  FD: First Parent or Father's Name Delimiter

6.  FN: First Parent or Father's Name as a single element

7.  FS: First Parent or Father's Surname

8.  M1: Mother's First Name

9.  MD: Mother's Name Delimiter

10. MN: Mother's Name as a single element

11. MS: Mother's Surname

12. OA: Ordinal, Absolute

13. OR: Ordinal, Relative

14. S1: Second Parent's First Name

15. SD: Second Parent's Name Delimiter

16. SN: Second Parent's Name as a single element

17. SS: Second Parent's Surname

18. SX: Suffix Start

S1, SD, SN and SS are intended to be alternatives to M1, MD, MN, and
MS.

Definitions
-----------
* First Name: Name identifying the name-bearer

* Middle Name: Second qualifier identifying the name-bearer

* Surname: Inter-generational name, or any other name used as an
  alternative where there are no inter-generational names. It is
  common to use a patronym in place.

* Ordinal: Indicator intended to distinguish between re-issued names.

Alternate Name Indexes
======================
Alternate names have a similar index convention to main names. In the
example name

``Katsushika Hokusai (hokusai, hokumoku, big.wav)``:

* There are three alternate names with the following indexes:

  * ``hokusai`` (index: 1)

  * ``hokumoku`` (2)

  * ``big.wav`` (3)

* Negative indexes are not supported

* Alternative names may be assigned with a network name.

  * The network are assigned with indexes with the prefix ``NN:``
    followed by the network (usually a host name).

  * Given a ``config_str`` of ``NN:example.com=2,NN:example.org=3``:

    * The index string ``example.com`` resolves to ``hokumoku``

    * ``example.org`` resolves to ``big.wav``

-----------
Other Notes
-----------

Spaces
======
Python conventions for classifying spaces apply. Any character that
falls under the Unicode category ``Zs``, or having a bidirectional
class of ``WS``, ``B`` or ``S`` is classified as a space.

For more information, go to:
https://docs.python.org/3/library/stdtypes.html#str.isspace

Titles
======
Titles will not be supported, as they are found to be application
and context-specific and beyond the scope of this specification.

--------
Examples
--------
TODO
