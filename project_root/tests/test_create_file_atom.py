
import unittest
import os
from app.atoms.create_file_atom import CreateFileAtom
import shutil

class TestCreateFileAtom(unittest.TestCase):
    def test_process(self):
        os.makedirs('test_dir', exist_ok=True)
        atom = CreateFileAtom()
        data = {'dir_name': 'test_dir', 'file_name': 'test.txt', 'content': 'test content'}
        result = atom.process(data)
        file_path = 'test_dir/test.txt'
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test content')
        os.remove(file_path)
        shutil.rmtree('test_dir')

if __name__ == '__main__':
    unittest.main()

