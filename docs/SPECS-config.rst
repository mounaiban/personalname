===============================================
PersonalName Configuration String Specification
===============================================
Version 1.23.2

------
Syntax
------
A Configuration String (config_str) contains zero or more options,
written as key-value pairs, as follows:

::

   CONFIG_1=VALUE_1;...;CONFIG_n=VALUE_n

All config_str should be encoded in Unicode.

In each key-value pair, an equal sign (U+003D) separates the key and
the value. Each pair is in turn separated with a semicolon (U+003B).
There should be no extra spaces. Keys must not begin with a space.

Separators cannot be set from a config_str; the separator symbols must
be set before the config_str is read.

Aliasing
========
It is possible to assign one value to multiple keys by using the
name of another key as the value, such as:

::

   A=1;B=A;C=A

which resolves to ``C1=1;C2=1;C3=1``

If the keys used as values cannot be resolved, the keys are
interpreted as values instead.

Please note that only one level of aliasing is supported. Strings
like ``A=1;B=A;C=B`` may not be read correctly.

Circular and Self References
----------------------------
Circular references are not allowed and should be interpreted as a
single-level alias; ``A=B;B=A`` should resolve to ``A=B;B=B`` (both A
and B have a value of a literal capital "B").

Self references are not allowed and should be interpreted as a literal
string value instead; ``A=A`` should resolve to key A with a value of
a literal capital "A".

Multiple Assignments
====================
Each key must only be used once. Subsequent assignments of the same
key is an error.

-----------------
Supported Options
-----------------
The following options listed below are supported. Please consult the
Name String specification for details on their meaning and usage.

* Main Name Element Type Assignments:
  N1, NM, NS, F1, FD, FN, FS, M1, MD, MN, MS, OA, OR, S1, SD, SN,
  SS, SX

* Alternate Name classifiers. These include all options beginning with
  "NN:".

* Alternate Name list separators: ALED, ALSE, ALST, MNSP, MNSU

Order of Appearance
-------------------
In a config_str dump, the order of elements begin with N1, NM then NS,
followed with the rest in ASCII/US English alphabetical order, numbers
first.

--------
Examples
--------

Basic Example Configuration Strings
===================================
Listed in Alphabetical Order

N1=1
N1=1;FD=2;F1=3;NS=4
N1=1;FD=2;F1=3;NS=F1
N1=1;FD=2;FS=3;MS=4
N1=1;FD=2;FS=3;MD=4;MS=5
N1=1;MS=2;FS=3;NS=FS
N1=1;NS=2
NS=1;N1=2
F1=1;N1=2;NS=F1
F1=1;N1=2;NS=3

Example with Social Media Profiles
==================================
NS=1;N1=2;NN:facebook.com=2;NN:tiktok.com=2

Complete Examples with Name Strings
===================================
TODO
