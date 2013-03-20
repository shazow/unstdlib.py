import sys
import unittest


sys.path.append('../')


from unstdlib.standard.collections_ import RecentlyUsedContainer


class TestRecentlyUsedContainer(unittest.TestCase):
    def test_maxsize(self):
        d = RecentlyUsedContainer(5)

        for i in xrange(5):
            d[i] = str(i)

        self.assertEqual(len(d), 5)

        for i in xrange(5):
            self.assertEqual(d[i], str(i))

        d[i+1] = str(i+1)

        self.assertEqual(len(d), 5)
        self.assertFalse(0 in d)
        self.assertTrue(i+1 in d)


if __name__ == '__main__':
    unittest.main()
