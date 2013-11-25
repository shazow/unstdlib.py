import sys
import unittest


sys.path.append('../')


from unstdlib.standard.collections_ import RecentlyUsedContainer
from unstdlib.standard.exception_ import convert_exception


class TestRecentlyUsedContainer(unittest.TestCase):
    def test_maxsize(self):
        d = RecentlyUsedContainer(5)

        for i in range(5):
            d[i] = str(i)

        self.assertEqual(len(d), 5)

        for i in range(5):
            self.assertEqual(d[i], str(i))

        d[i+1] = str(i+1)

        self.assertEqual(len(d), 5)
        self.assertFalse(0 in d)
        self.assertTrue(i+1 in d)


class TestException_(unittest.TestCase):

    def test_convert_exception(self):

        class FooError(Exception):
            pass

        class BarError(Exception):
            def __init__(self, message):
                self.message = message

        @convert_exception(FooError, BarError, message='bar')
        def throw_foo():
            raise FooError('foo')

        try:
            throw_foo()
        except BarError as e:
            self.assertEqual(e.message, 'bar')


if __name__ == '__main__':
    unittest.main()
