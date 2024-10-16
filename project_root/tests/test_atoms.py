# Filename: test_atoms.py\n# Path: project_root/tests/test_atoms.py\n# Log Level: INFO\n
import unittest
import os
from app.atoms.create_directory_atom import CreateDirectoryAtom
from app.atoms.create_file_atom import CreateFileAtom

class TestCreateDirectoryAtom(unittest.TestCase):
    def test_process(self):
        atom = CreateDirectoryAtom()
        data = {'dir_name': 'test_dir'}
        result = atom.process(data)
        self.assertTrue(os.path.exists('test_dir'))
        self.assertEqual(result['status'], "Directory 'test_dir' ensured.")
        os.rmdir('test_dir')

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
        os.rmdir('test_dir')

