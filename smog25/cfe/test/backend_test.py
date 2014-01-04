import pickle
import unittest

from smog25.cfe import backend


class PickledStreamReaderTest(unittest.TestCase):

    def setUp(self):
        self.objects = []
        self.reader = backend.PickledStreamReader(self.new_object) 
    
    def new_object(self, obj):
        self.objects.append(obj)

    def test_feeding(self):
        obj1 = (123, {1: 'a'})
        obj2 = [obj1, obj1]
        str1 = pickle.dumps(obj1)
        str2 = pickle.dumps(obj2, pickle.HIGHEST_PROTOCOL)
        self.reader.feed(str1[:-5])
        self.assertEqual(self.objects, [])
        self.reader.feed(str1[-5:] + str2[:5])
        self.assertEqual(self.objects, [obj1])
        self.reader.feed(str2[5:])
        self.assertEqual(self.objects, [obj1, obj2])
        self.assertEqual(self.reader._buffer.tell(), 0)

if __name__ == "__main__":
    unittest.main()
