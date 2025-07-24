
import unittest
from app.atoms.sort_by_size_atom import SortBySizeAtom

class TestSortBySizeAtom(unittest.TestCase):
    def test_process(self):
        data = {'items': [
            {'filename': 'file1', 'size': 200},
            {'filename': 'file2', 'size': 100},
            {'filename': 'file3', 'size': 300}
        ]}
        atom = SortBySizeAtom()
        result = atom.process(data)
        sorted_items = result['sorted_items']
        self.assertEqual(sorted_items[0]['filename'], 'file3')
        self.assertEqual(sorted_items[1]['filename'], 'file1')
        self.assertEqual(sorted_items[2]['filename'], 'file2')

if __name__ == '__main__':
    unittest.main()

