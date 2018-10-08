import re
import unittest
from ...core.options import _mergeOpts, _normalizeOpts, Options


class TestOptions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_mergeOpts(self):
        # should convert tuple to dict and merge child with parent
        result = _mergeOpts((('a', 1), ('b', {'a': 2})), 'b')
        self.assertEqual(result.a, 2)
        self.assertNotIn('b', result)
        # should merge child option a with the parent options (dict)
        result = _mergeOpts({'a': 1, 'b': {'a': 2}}, 'b')
        self.assertEqual(result.a, 2)
        self.assertNotIn('b', result)
        # should include child option c and d with the parent options (dict)
        result = _mergeOpts({'a': 1, 'b': {'c': 2, 'd': 3}}, 'b')
        self.assertEqual(result.a, 1)
        self.assertEqual(result.c, 2)
        self.assertEqual(result.d, 3)
        self.assertNotIn('b', result)
        # should merge child option a and include c as parent options (dict)
        result = _mergeOpts({'a': 1, 'b': {'a': 2, 'c': 3}}, 'b')
        self.assertEqual(result.a, 2)
        self.assertEqual(result.c, 3)
        self.assertNotIn('b', result)
        # should merge Options instance with child dict key
        instance = Options()
        instance.a = {'disabled': True}
        result = _mergeOpts(instance, 'a')
        self.assertEqual(result.disabled, True)
        self.assertNotIn('a', list(getattr(result, '__dict__', {})))

    def test_normalizeOpts(self):
        # should replace key with - to _ in dict
        result = _normalizeOpts({
            'a-b': 1
        })
        self.assertEqual(result['a_b'], 1)
        self.assertNotIn('a-b', result)
        # should replace key with - to _ in Options instance
        instance = Options()
        setattr(instance, 'a-b', 1)
        result = _normalizeOpts(instance)
        self.assertEqual(result.a_b, 1)
        self.assertNotIn('a-b', list(getattr(result, '__dict__', {})))
        # should do nothing
        result = _normalizeOpts({
            'a_b': 1
        })
        self.assertEqual(result['a_b'], 1)

    def test__get_boolean(self):
        # should return default value since no option
        self.assertEqual(Options()._get_boolean('a'), False)
        # should return true as default since no option
        self.assertEqual(Options()._get_boolean('a', True), True)
        # should return false as in option
        self.assertEqual(Options({'a': False})._get_boolean('a', True), False)

    def test__get_characters(self):
        # should return default value since no option
        self.assertEqual(Options()._get_characters('a'), '')
        # should return \'character\' as default since no option
        self.assertEqual(Options()._get_characters(
            'a', 'character'), 'character')
        # should return \'char\' as in option
        self.assertEqual(Options({'a': 'char'})._get_characters(
            'a', 'character'), 'char')

    def test__get_number(self):
        # should return default value since no option
        self.assertEqual(Options()._get_number('a'), 0)
        # should return 1 as default since no option
        self.assertEqual(Options()._get_number('a', 1), 1)
        # should return 10 as in option
        self.assertEqual(Options({'a': 10})._get_number('a', 1), 10)
        # should return 0 for NaN as in option
        self.assertEqual(Options({'a': 'abc'})._get_number('a'), 0)
        # should return 0 for NaN as in default
        self.assertEqual(Options()._get_number('a', 'abc'), 0)

    def test__get_array(self):
        # should return [] with no option
        self.assertEqual(Options()._get_array('a'), [])
        # should return [\'a\',\'b\'] as default since no option
        self.assertEqual(Options()._get_array('a', ['a', 'b']), ['a', 'b'])
        # should return [\'c\',\'d\'] as in option
        self.assertEqual(Options({'a': ['c', 'd']})._get_array(
            'a', ['a', 'b']), ['c', 'd'])
        # should return [\'c\',\'d\'] as in option comma separated
        self.assertEqual(Options({'a': 'c,d'})._get_array(
            'a', ['a', 'b']), ['c', 'd'])

    def test__is_valid_selection(self):
        # should return false with empty selection
        self.assertEqual(Options()._is_valid_selection(['a', 'b'], []), False)
        # should return false with selection inexistent
        self.assertEqual(Options()._is_valid_selection(
            ['a', 'b'], ['c']), False)
        # should return true with selection existent
        self.assertEqual(Options()._is_valid_selection(
            ['a', 'b'], ['a', 'b']), True)

    def test__get_selection_list(self):
        # should raise error with empty selection
        with self.assertRaisesRegexp(ValueError, 'Selection list cannot'
                                     + ' be empty.'):
            Options()._get_selection_list('a', [])
        # should raise error with invalid default
        with self.assertRaisesRegexp(ValueError, 'Invalid Default Value!'):
            Options()._get_selection_list('a', ['a', 'b'], ['c'])
        # should raise error with invalid option
        with self.assertRaisesRegexp(ValueError, '^Invalid Option Value:'
                                     + ' The option'):
            Options({'a': ['c', 'd']})._get_selection_list(
                'a', ['a', 'b'], ['a', 'b'])
        # should return [\'c\'] as in option
        opts = Options({'c': ['c']})
        self.assertEqual(opts._get_selection_list(
            'c', ['c', 'd'], ['c']), ['c'])

    def test__get_selection(self):
        # should raise error with multiple selection
        with self.assertRaisesRegexp(ValueError, '^Invalid Option'
                                     + ' Value: The option'):
            Options({'a': ['a', 'b']})._get_selection('a', ['a', 'b'], ['a'])
        # should return [\'a\'] as in option
        options = Options({'a': ['a']})
        self.assertEqual(options._get_selection(
            'a', ['a', 'b'], ['a']), 'a')


if __name__ == '__main__':
    unittest.main()
