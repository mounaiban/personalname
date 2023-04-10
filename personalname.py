"""
Personal Name Class for Python

An object for processing personal names of varying formats

"""
# Copyright 2023 by Moses Chong
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#
# Please use Python 3.7 or later (where built-in dict is ordered)
# for correct operation.
# Ref: https://docs.python.org/3.7/library/collections.html#ordereddict-objects
#
# This module uses spaces, not tabs

class PersonalName:
    """
    The PersonalName Class for Python, for flexible handling of
    personal names of varying formats. Please refer to README.rst or
    the Technical Documentaion for a more detailed explanation on
    usage and implementation.

    """
    CONFIG_SEP = '\u003b'     # ; semicolon
    CONFIG_KV_SEP = '\u003d'  # = equals
    CONFIG_DEFAULT = { # configurables and their default values
        'ALED': '\u0029',  # Alt Name List End: ) right parenthesis
        'ALSE': '\u002C',  # Alt Name List Separator: , comma
        'ALST': '\u0028',  # Alt Name List Start: ( left parenthesis
        'MNSP': '\u0020',  # Main Name Space: ASCII space
        'MNSU': '\u005f',  # Main Name Space Substitute: _ underscore
    }
    OUT_DEFAULT = ''       # Returned value for invalid indexes
    INDEXES_MAIN_NAME = (  # Main Name Element Types also used as index keys
        'N1', # First Name
        'NM', # Middle Name
        'NS', # Surname
        #
        'F1', # First Parent or Father's First Name
        'FD', # First Parent/Father's Name Delimiter (e.g. Anak, de, ibn, von..)
        'FN', # First Parent or Father's Name as a single element
        'FS', # Father's Surname
        'M1', # Mother's First Name
        'MD', # Mother's Name Delimiter (e.g. y)
        'MN', # Mother's Name as a single element
        'MS', # Mother's Surname
        'OA', # Ordinal (absolute, e.g. I, II, III,...)
        'OR', # Ordinal (relative, e.g. Jr., Sr.)
        'S1', # Second Parent's First Name               |
        'SD', # Second Parent's Name Delimiter           | alternative to
        'SN', # Second Parent's Name as a single element | M1, MD, MN, MS
        'SS', # Second Parent's Surname                  |
        'SX', # Suffix Start (use as fallback only!)
    )
    NICKNAME_PREFIX = 'NN'
    NICKNAME_NET_DELIM = '\u003a' # Nickname Network Delimiter: ASCII colon
    NOT_PRESENT = None

    def __init__(self, name_str, config_str="", **kwargs):
        """
        PersonalName examples:

        a = PersonalName('Andre Konstantinovich Geim', 'N1=1;FN=2;NS=3')
        #
        # First Name (N1): Andre
        # Combined Patronym (FN): Konstantinovich
        #       (includes Father's Name and suffix Delimiter)
        # Surname (NS): Geim

        d = PersonalName('Inoue Daisuke', 'NS=1;N1=2')
        #
        # Surname (NS): Inoue; First Name (N1): Daisuke

        g = PersonalName('Gauri Nanda (clocky)', 'N1=1;NS=2')
        #
        # N1: Gauri; NS: Nanda; Main (and sole) nickname: 'clocky'

        m = PersonalName(
            'Maria Viktorovna (GentleWhispering, maria.gentlewhispering)',
            'N1=1;FN=2;NS=FN;NN:youtube.com=1,NN:instagram.com=2'
        )
        # N1: Maria; FN: Viktorovna; FN used as NS
        # Identifies as handle 'GentleWhispering' on network youtube.com,
        # 'maria.gentlewhispering' on network instagram.com

        s = PersonalName('Soo Tsu_Hong (Lisa)', 'NS=1;N1=2')
        #
        # NS: Soo; N1: Tsu Hong; Main Alternate Name: Lisa
        # Spaces inside elements are written with a space substitute,
        # an underscore by default. These are converted to spaces
        # when the name or element is retrieved.

        Please note that the first element has an index of one.
        Zero indexes are reserved and are not in use.

        For a list of supported element index types, please see
        INDEXES_MAIN_NAME, or the Configuration String specification
        in the Technical Documentation.

        Args
        ----
        * name_str: Name String in Unicode, and in this format:

          main_name (alt_name_0, ... alt_name_N)

          main_name is a series of zero or more words or initials,
          herein called 'elements'. By default, elements are separated
          by spaces (U+0020) and spaces within elements are represented
          by underscores (U+005F).

          alt_names are optional alternate names. Multiple alt_names
          are separated by commas (U+002C) by default.

          The delimiters may be configured using config_str; please
          see the Technical Documentation for details.

        * config_str: Configuration String in this format:

          c_0=v_0;...;c_N=v_N

          The string contains a list of zero or more configuration
          key-value pairs with equal signs (U+003D) between keys and
          values separated by semicolons (U+003B) by default.

          The config_str is used primarily for marking up main names
          and assigning types to the name's elements. It may also be
          used for changing the delimiter characters of the list of
          alternate names.

          The Name String and Configuration String Specifications
          in the Technical Documentation explains supported keys in
          greater detail.

        No other arguments are currently supported

        """
        self.name_string = name_str   # in Unicode
        #
        # Configuration
        self._config = {}
        self._tdict: dict
        self._tdict_in: dict
        self._i_alt_list_start = len(self.name_string)
        self._i_alt_list_end = self._i_alt_list_start
        self._set_config(self.parse_config(config_str))

    def __repr__(self):
        out = ''
        return "{}({}, {})".format(
            self.__class__.__name__,
            self.name_string or "''",
            self.get_config_str() or "''"
        )

    def _main_name_iter(self):
        s = self._i_alt_list_start
        return (x for x in self.name_string[:s].split() if not x.isspace())

    def _alt_name_iter(self):
        s = self._i_alt_list_start
        e = self._i_alt_list_end
        return (x for x in self.name_string[s+1:e].split(self._config['ALSE']) if x and not x.isspace())

    def _set_config(self, config_dict):
        """
        Apply configuration settings from config_dict to the name's
        configuration.

        Supported settings that are not present config_dict will
        be left unchanged if already set, or set to defaults
        otherwise.

        Please see CONFIG_DEFAULT for defaults and supported settings.

        """
        # set delimiters and separators
        for k in self.CONFIG_DEFAULT:
            if k in config_dict: self._config[k] = config_dict[k]
            elif k in self._config: pass
            else: self._config[k] = self.CONFIG_DEFAULT[k]
        # set main name elements
        for k in self.INDEXES_MAIN_NAME:
            if k in config_dict: self._config[k] = config_dict[k]
            elif k not in config_dict: self._config[k] = self.NOT_PRESENT
            elif k in self._config: pass
        # set nicknames
        for n in (x for x in config_dict if x.startswith(self.NICKNAME_PREFIX)):
            self._config[n] = config_dict[n]
        self._tdict = {ord(self._config['MNSU']): self._config['MNSP']}
        self._tdict_in = {ord(self._config['MNSP']): self._config['MNSU']}
        if self._config['ALST'] in self.name_string:
            self._i_alt_list_start = self.name_string.index(
                self._config['ALST']
            )
            self._i_alt_list_end = self.name_string.index(
                self._config['ALED'], self._i_alt_list_start
            )

    def get_config_str(self):
        """
        Get the shortest possible config_str required to reproduce
        this name's configuration. Options that are not set or left
        at defaults will not be included.

        """
        # PROTIP: this method is public as it is a multi-lang test subject
        out = ''
        cv_fmt_L1 = "{}{}{}{}".format(
            '{}', self.CONFIG_KV_SEP, '{}', self.CONFIG_SEP
        )
        # configuration
        for k in self.CONFIG_DEFAULT.keys():
            if self._config[k] != self.CONFIG_DEFAULT[k]:
                out = ''.join((out, cv_fmt_L1.format(k, self._config[k])))
        # main name element indices
        for k in (x for x in self._config if x in self.INDEXES_MAIN_NAME):
            if self._config[k]:
                out = ''.join((out, cv_fmt_L1.format(k, self._config[k])))
        # nicknames
        it = (x for x in self._config if x.startswith(self.NICKNAME_PREFIX))
        for k in it:
            out = ''.join((out, cv_fmt_L1.format(k, self._config[k])))
        return out[:-1]

    def count_main_name_elements(self):
        nit = self._main_name_iter()
        i = 0
        for x in nit: i += 1
        return i

    def count_alt_names(self):
        nit = self._alt_name_iter()
        i = 0
        for x in nit: i += 1
        return i

    def parse_config(self, config_str):
        """
        Parse configuration string into a dict

        Please consult the Configuration String Specification in the
        Technical Documentation for details on the string format.

        """
        # PROTIP: this method is public as it is a multi-lang test subject
        if not config_str: return {}
        out = {}
        for opt in config_str.split(self.CONFIG_SEP):
            k, v = opt.split(self.CONFIG_KV_SEP)
            if k in out:
                raise KeyError("option {} already set".format(k))
            else:
                out[k] = v
        for k in out:
            if out[k] in out:
                # Resolve aliases
                v = out[k]
                if v == k: pass          # treat self-alias as literal
                elif out[v] in out: pass # only one level of aliases allowed
                else: out[k] = out[v]
            if (k in self.INDEXES_MAIN_NAME
                or k.startswith(self.NICKNAME_PREFIX)):
                    try:
                        out[k] = int(out[k])
                    except ValueError:
                        raise ValueError("index {} must be integer".format(k))
        return out

    def get_formatted_name(self, fmt):
        """
        Returns the name in a user-nominated format, according to
        a format string.

        Example:
        a = PersonalName('Andre Konstantinovich Geim', 'N1=1;FN=2;NS=3')

        a.get_formatted_name("{N1} {NS}") => 'Andre Geim'
        a.get_formatted_name("{N1} {PD} {FN}") => 'Andre  Konstantinovich'
            # note the two spaces

        Format Code
        -----------
        Format tags are enclosed by curly brackets (as seen in Python
        and CSharp). Suported tags found in the format string will be
        substituted with an element. Tags for undefined elements will
        be removed.

        Malformed or unsupported tags will be passed on to the output.

        """
        # TODO: support alternate names too?
        out = ''
        TOPEN = '\u007b'   # { ASCII left curly bracket
        TCLOSE = '\u007d'  # } ASCII right curly bracket
        i = 0
        last_topen = 0
        last_tclose = 0
        try:
            while i < len(fmt):
                # consider everything between the next tag close,
                # and the last tag open before it as the whole tag.
                last_topen = fmt.index(TOPEN, last_tclose)
                last_tclose = fmt.index(TCLOSE, last_topen)
                last_topen = fmt.rfind(TOPEN, last_topen, last_tclose)
                infix = fmt[last_topen:last_tclose+1]
                el_type = infix[1:-1]
                if el_type in self.INDEXES_MAIN_NAME:
                    infix = self.get_main_name_element(el_type)
                out = ''.join((out, fmt[i:last_topen], infix))
                i = last_tclose + 1
        except ValueError:
            # no more substitutions
            out = ''.join((out, fmt[i:]))
        return out

    def get_main_name_element(self, i):
        """
        Return a single element (component) of the main name of a
        specific type, or by numerical index. Elements will be
        returned in presentation-ready form with spaces in place
        of space substitutes.

        e = PersonalName(
            'Enrique Miguel Iglesias Preysler',
            'N1=1;NM=2;PS=3;MS=4;NS=PS'
        )

        e.get_main_name_element(-1) => 'Preysler'
        e.get_main_name_element(-2) => 'Iglesias'
        e.get_main_name_element('N1') => 'Enrique'
        e.get_main_name_element(1) => 'Enrique'

        """
        if issubclass(type(i), str):
            # Resolve name to value
            if i == self.NICKNAME_PREFIX:
                raise KeyError('{}: use get_alt_name for alternate names'.format(i))
            if i in self.INDEXES_MAIN_NAME:
                i = self._config.get(i, self.NOT_PRESENT)
                if not i: return self.OUT_DEFAULT
            else: raise KeyError('unsupported element')
        if not i: raise IndexError('first element is one')
        nit: iter
        return self.get_main_name_elements_as_str(i, i)

    def get_main_name_elements_as_str(self, s, e, sep=' '):
        """
        Return multiple elements (components) of the main name by
        numerical index, from s to e inclusive. The first element
        of the main name has an index of one (1).

        Negative indexes are also supported; these address the main
        name elements from the end to the start. The index of the
        last element is -1.

        Positive and negative indexes cannot be used together,
        except for when e is -1.

        Out-of-bounds indexes are substituted for the highest (or
        lowest for negative indexes) index possible.

        e = PersonalName('Enrique Miguel Iglesias Preysler')
        e.get_main_name_elements_as_str(1, 2) => 'Enrique Miguel'
        e.get_main_name_elements_as_str(-2, -1) => 'Iglesias Preysler'
        e.get_main_name_elements_as_str(2, -1) => 'Miguel Iglesias Preysler'

        The separator can be changed by setting sep, the default
        is an ASCII space (U+0020).

        """
        out = ""
        n = e-s
        # reject invalid start and end settings
        if s > e and e != -1: raise IndexError('start must come before end')
        elif (s < 1 and e >= 1) or (s >= 1 and e < 1) and e!= -1:
            raise IndexError('cannot use positive with negative indices')
        # get elements
        try:
            if s < 1:
                mend = self._i_alt_list_start
                nit = (x for x in reversed(self.name_string[:mend].split()) if not x.isspace())
                for x in range(e+1, 0): next(nit) # skip
                for x in range(n+1):
                    out = ''.join((next(nit), sep, out))
                out = out.rstrip()
            else:
                nit = self._main_name_iter()
                for x in range(s-1): next(nit) # skip
                if e == -1:
                    for x in nit:
                        out = ''.join((out, sep, x))
                else:
                    for x in range(n+1):
                        out = ''.join((out, sep, next(nit)))
                out = out.lstrip()
        except StopIteration:
            pass
        finally:
            return out.translate(self._tdict)

    def get_main_name_element_type(self, el):
        """
        Returns the type of the main name element

        Example:
        d = PersonalName('Inoue Daisuke', 'NS=1;N1=2')
        d.get_main_name_element_type('Daisuke') => 'N1'

        If an element is of multiple types, the types will be
        separated by semicolons by default, in order of
        appearance in self.INDEXES_MAIN_NAME (e.g. 'NS;PS').

        Spaces are automatically converted to space substitutes
        before the lookup.

        """
        # This method is currently implemented as a slow linear search,
        # but it has been deemed acceptable for now as the method is
        # not expected to be frequently used, and most names are not
        # expected to have a large number of elements.
        el = el.translate(self._tdict_in)
        nit = self._main_name_iter()
        i = 1
        for e in nit:
            if e == el:
                out = ''
                for k in self.INDEXES_MAIN_NAME:
                    if k in self._config and self._config[k] == i:
                        out = ''.join((out, k, self.CONFIG_SEP))
                return out[:-1]
            i += 1
        raise ValueError('element {} not found in main name'.format(el))

    def get_alt_name(self, i=1):
        """
        Return an alternate name associated with index i.
        When i is not specified, return the first alternate name.
        i may be a numeric index or a network nickname.

        Example:
        m = PersonalName(
            'Moshe Cohen (Goat Man, thegoat1)', 'N1=1;NS=2;NN:example.com=2;'
        )
        m.get_alt_name() => 'Goat Man'
        m.get_alt_name(1) => 'Goat Man'
        m.get_alt_name(2) => 'thegoat1'
        m.get_alt_name('example.com') => 'thegoat1' # net nick for example.com

        """
        if issubclass(type(i), str):
            # resolve network name to index
            nn_fq = ''.join(
                (self.NICKNAME_PREFIX, self.NICKNAME_NET_DELIM, i)
            )
            if nn_fq not in self._config:
                return self.OUT_DEFAULT
            else: i = self._config.get(nn_fq)
        elif self._i_alt_list_start == len(self.name_string):
            raise IndexError('no alternate names found')
        elif i < 1: raise IndexError('first element is one')
        s = self._i_alt_list_start
        e = self._i_alt_list_end
        try:
            anit = self._alt_name_iter()
            for x in range(i-1):
                next(anit)
            return next(anit).strip()
        except StopIteration:   # end of names reached
            return self.OUT_DEFAULT

    def get_main_name(self):
        """
        Return the main name in a presentation-ready form with spaces
        """
        i = self._i_alt_list_start
        return self.name_string[:i].strip().translate(self._tdict)

    def get_main_name_nosp(self):
        """
        Return the main name without spaces

        Originally intended for names written in Chinese and Korean,
        this is expected to be be useful for other languages where
        names are written without spaces.

        """
        td = {ord(self._config['MNSP']): None}
        return self.get_main_name().translate(td)
