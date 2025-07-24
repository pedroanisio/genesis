
import unittest
import os
from app.atoms.list_mkv_files_atom import ListMkvFilesAtom

class TestListMkvFilesAtom(unittest.TestCase):
    def test_process(self):
        os.makedirs('test_dir', exist_ok=True)
        file_path = 'test_dir/test.mkv'
        with open(file_path, 'w') as f:
            f.write('test content')
        atom = ListMkvFilesAtom()
        data = {'dir_name': 'test_dir'}
        result = atom.process(data)
        self.assertIn('items', result)
        self.assertEqual(len(result['items']), 1)
        self.assertEqual(result['items'][0]['filename'], 'test.mkv')
        os.remove(file_path)
        os.rmdir('test_dir')

if __name__ == '__main__':
    unittest.main()

