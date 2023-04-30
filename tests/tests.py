import builtins
import __main__
from json import JSONDecoder, decoder
from os import scandir
from personalname import PersonalName
from unittest import TestCase

classes = (PersonalName,)
exceptions = {
    'any': Exception,
    'arithmetic': ArithmeticError,
    'index': IndexError,
    'key': KeyError,
    'type': TypeError,
    'value': ValueError,
}
jd = JSONDecoder()

class data_defined_tests(TestCase):
    def test_all(self):
        for c in classes: 
            tdata: dict
            tfiles = [f for f in scandir('tests/') if f.name.startswith(c.__name__) and f.name.endswith('.json')]
            for f in tfiles:
                with open(f.path, mode='r') as h:
                    try:
                        tdata = jd.decode(h.read())
                        for test in tdata.get('tests', {}):
                            with self.subTest(test=test,file=f.path):
                                tspecs = tdata['tests'][test]
                                obj = c(**tspecs.get('init', {}))
                                fn = getattr(obj, tspecs['fn_name'])
                                kwargs = tspecs.get('args', {})
                                # TODO: multiple calls are not yet implemented
                                if 'exception' in tspecs:
                                    with self.assertRaises(
                                        exceptions[tspecs['exception']]
                                    ):
                                        print(fn(**kwargs))
                                else:
                                    self.assertEqual(
                                        fn(**kwargs), tspecs['out']
                                    )
                    except(decoder.JSONDecodeError) as jde:
                        jde.add_note("error in test file {}".format(f.path))
                        raise jde
