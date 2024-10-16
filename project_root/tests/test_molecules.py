# Filename: test_molecules.py\n# Path: project_root/tests/test_molecules.py\n# Log Level: INFO\n
import unittest
from app.molecules.base_molecule import SequentialMolecule
from app.atoms.create_directory_atom import CreateDirectoryAtom
from app.atoms.create_file_atom import CreateFileAtom

class TestSequentialMolecule(unittest.TestCase):
    def test_run(self):
        data = {
            'dir_name': 'test_dir',
            'file_name': 'test_file.txt',
            'content': 'Test Content'
        }

        molecule = SequentialMolecule()
        molecule.add_atom(CreateDirectoryAtom())
        molecule.add_atom(CreateFileAtom())
        result = molecule.run(data)

        self.assertTrue(os.path.exists('test_dir/test_file.txt'))
        with open('test_dir/test_file.txt', 'r') as file:
            content = file.read()
        self.assertEqual(content, 'Test Content')

        # Cleanup
        os.remove('test_dir/test_file.txt')
        os.rmdir('test_dir')

