==========================================
Using PNTK for Names in Multiple Languages
==========================================

Each Name String only encodes a single name in a single language.
If there are different versions of a name for different languages,
it is recommended to use a different name string for each language.

On platforms with built-in support for string-addressed arrays
(e.g. JavaScript objects and Python dict's), the current
recommendation is to keep each translation of the same name in the
same object, with IETF BCP 47 language codes as the value keys.

Here is an example in JSON:
::

    {
        "en": ["Victor Chang (vchang)", "fnln;NN:example.com=1"],
        "zh": ["張 任謙", "lnfn-nosp"],
    },

In this example, the strings have been abbreviated for normalisation
across many names and to improve space-efficiency.  These are the
expansions:

::

    {
        "lnfn": "NS=1;N1=2",
        "fnln": "N1=1;NS=2"
    }

The -nosp is an indication that the main name is to be printed without
spaces.

----------
References
----------
Wikipedia. IETF language tag. https://en.wikipedia.org/wiki/IETF_language_tag
