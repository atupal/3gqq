
import unittest
import sys
import os
sys.path.append(os.path.realpath('../'))
import application

class _3gqq67TestCase(unittest.TestCase):
    def setUp(self):
        self.app =  application.app.test_client()

    def tearDown(self):
        pass

    def test_1(self):
        assert 'select' in self.app.get('/').data

    def test_2(self):
        self.app.get('/')

    def test_3(self):
        self.app.get('/')

if __name__ == "__main__":
    unittest.main()
