=====================
Personal Name Toolkit
=====================

--------
Overview
--------
The PNTK is a little collection of programs to handle personal names
across different formats. Its main aim is to explore a particular
method of allowing systems to correctly process names not in the the
First Name-Last Name format, alongside names that are, in the most
frictionless way possible.

An object-oriented Python reference implementation is currently
available, with implementations in more languages to be added in
due course.

The PNTK is Free Software, licensed under the terms and conditions
of the GNU Lesser General Public License, Version 3 or later.
The full terms and conditions are in COPYING and COPYING.LESSER,
or at https://www.gnu.org/licenses.

------------
How It Works
------------
PNTK deals with names in two parts: a name string, and a
configuration string. The name string contains a main name and an
optional list of alternate names, all in a single Unicode string.

The configuration string contains markup information that
classifies the different parts of the name.

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

-------------
Documentation
-------------
Some detailed technical information may be found in the Python
reference module. For specifications, usage guidelines and detailed
examples please check the Technical Documentation in the ``/docs``
directory.
