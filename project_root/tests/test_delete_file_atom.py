
import unittest
import os
from app.atoms.delete_file_atom import DeleteFileAtom
import shutil

class TestDeleteFileAtom(unittest.TestCase):
    def test_process(self):
        os.makedirs('test_dir', exist_ok=True)
        file_path = 'test_dir/test.txt'
        with open(file_path, 'w') as f:
            f.write('test content')
        atom = DeleteFileAtom()
        data = {'file_path': file_path}
        result = atom.process(data)
        self.assertFalse(os.path.exists(file_path))
        shutil.rmtree('test_dir')

if __name__ == '__main__':
    unittest.main()

