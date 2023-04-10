=====================
Personal Name Toolkit
=====================

--------
Overview
--------
The PNTK is an attempt at a standard to handle personal names across
different formats, inspired by a need for a method for correctly
processing names not in the the First Name-Last Name format,
alongside names that are, in the most frictionless way possible.

An object-oriented Python reference implementation is currently
available, with implementations in more languages to be added in
due course.

All example implementations of the PNTK in this repository are Free
Software, licensed under the terms and conditions of the GNU Lesser
General Public License, Version 3 or later.

The full terms and conditions are in ``COPYING`` and
``COPYING.LESSER``, or at https://www.gnu.org/licenses.

------------
How It Works
------------
PNTK deals with names in two parts: a name string, and a configuration
string. The name string contains a main name and an optional list of
alternate names, all in a single Unicode string.

The configuration string contains markup information that classifies
the different components (herein called 'elements') of the name.
Keeping the configuration string separate from the name string allows
normalisation and sharing of config strings across multiple names.

Names are preserved in their original issued format.

Examples
========

Muhammad ibn Abu Bakr al-Khwarizmi
----------------------------------
This name contains a first name followed by a patronym and a surname,
with a social network nickname

Name String: ``Muhammad ibn Abu_Bakr al-Khwarizmi (0effort)``

* Config String: ``N1=1;FD=2;F1=3;NS=4;NN:example.com=1``

* First Name (N1): Muhammad

* Father's name delimiter (PD): ibn

* Father's first name (F1): Abu Bakr

* Surname (NS): al-Khwarizmi

* Alternate Name: 0effort (nickname on example.com)

Katsushika Hokusai
------------------
This name begins with a surname, followed by the first name

Name String: ``Katsushika Hokusai``

* Config String: ``NS=1;N1=2``

* First Name (N1): Hokusai

* Surname (NS): Katsushika

* No alternate names provided

The config strings may be normalised and reused, as naming formats are
consistent across many names.

Standard Functions/Methods
==========================
This is a list of core functions (methods on object-oriented
platforms) that defines the PNTK. The first main name element and
the first alternate name have an index of one (1).

For more details, please refer to the Python reference module,
``personalname.py``.

 PROTIP: This list was derived from the Python reference
 implementation by running:

 ``for x in sorted(dir(PersonalName)): print (f"{x}")``

``count_alt_names()``
---------------------
Non-OO alternative: ``count_alt_names(name_str)``

Returns the number of alternate names

``count_main_name_elements()``
------------------------------
Non-OO alternative: ``count_main_name_elements(name_str)``

Returns the number of elements in the main name

``get_alt_name(i)``
-------------------
Non-OO alternative: ``get_alt_name(name_str, config_str, i)``

Returns an alternate name by numeric index or network name

``get_config_str()``
--------------------
Non-OO alternative: ``get_config_str(config)``

Returns the shortest string required to reproduce a personal name
object or environment's configuration.

``get_formatted_name(fstr)``
----------------------------
Non-OO alternative: ``get_formatted_name(name_str, config_str, fstr)``

Returns a variation of the main name conforming to a specific format
defined by ``fstr``

``get_main_name()``
------------------
Non-OO alternative: ``get_main_name(name_str)``

Returns the main name

``get_main_name_element(i)``
----------------------------
Non-OO alternative: ``get_main_name_element(name_str, config_str, i)``

Returns the main name by element type or by numeric index

``get_main_name_element_type(el)``
----------------------------------
Non-OO alternative: ``get_main_name_element(name_str, config_str, el)``

Returns the type of an element in the main name

``get_main_name_elements_as_str(s, e)``
---------------------------------------
Non-OO alternative: ``get_main_name_elements_as_str(name_str, s, e)``

Returns consecutive elements in the main name between s and e, in a
single string

``get_main_name_nosp()``
------------------------
Non-OO alternative: ``get_main_name_nosp(name_str)``

Returns the main name, but without spaces

``parse_config(config_str)``
----------------------------
Parses a configuration string. On object-oriented platforms this
configures a personal name object, on non-OO platforms this returns a
key-value store or string-addressable array.

-------------
Documentation
-------------
Some detailed technical information may be found in the Python
reference module. For specifications, usage guidelines and detailed
examples please check the Technical Documentation in the ``/docs``
directory.
