#!/bin/bash

# Define base directory
BASE_DIR="project_root"

# Create directories
declare -a DIRS=(
    "$BASE_DIR/app"
    "$BASE_DIR/app/atoms"
    "$BASE_DIR/app/molecules"
    "$BASE_DIR/tests"
    "$BASE_DIR/logs"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo "Created directory: $dir"
done

# Function to create files with headers and content
create_file_with_content() {
    local file_path=$1
    local content=$2
    echo "$content" > "$file_path"
    echo "Created file: $file_path"
}

# Content for each file

# __init__.py files
init_content="# Filename: __init__.py\n# Path: $BASE_DIR/app/__init__.py\n# Log Level: DEBUG\n\n# Initialization for the app module."
create_file_with_content "$BASE_DIR/app/__init__.py" "$init_content"

init_atoms_content="# Filename: __init__.py\n# Path: $BASE_DIR/app/atoms/__init__.py\n# Log Level: DEBUG\n\n# Initialization for atoms module."
create_file_with_content "$BASE_DIR/app/atoms/__init__.py" "$init_atoms_content"

init_molecules_content="# Filename: __init__.py\n# Path: $BASE_DIR/app/molecules/__init__.py\n# Log Level: DEBUG\n\n# Initialization for molecules module."
create_file_with_content "$BASE_DIR/app/molecules/__init__.py" "$init_molecules_content"

init_tests_content="# Filename: __init__.py\n# Path: $BASE_DIR/tests/__init__.py\n# Log Level: DEBUG\n\n# Initialization for tests module."
create_file_with_content "$BASE_DIR/tests/__init__.py" "$init_tests_content"

# BaseAtom class
base_atom_content="# Filename: base_atom.py\n# Path: $BASE_DIR/app/atoms/base_atom.py\n# Log Level: INFO\n
from abc import ABC, abstractmethod
import logging

class Atom(ABC):
    @abstractmethod
    def execute(self, data: dict):
        pass

class BaseAtom(Atom):
    def __init__(self, name: str):
        self.name = name

    def execute(self, data: dict) -> dict:
        logging.info(f'Executing atom: {self.name}')
        try:
            return self.process(data)
        except Exception as e:
            logging.error(f'Error in atom \"{self.name}\": {e}')
            raise RuntimeError(f'Failed to execute atom \"{self.name}\"')

    @abstractmethod
    def process(self, data: dict) -> dict:
        pass
"
create_file_with_content "$BASE_DIR/app/atoms/base_atom.py" "$base_atom_content"

# CreateDirectoryAtom class
create_directory_atom_content="# Filename: create_directory_atom.py\n# Path: $BASE_DIR/app/atoms/create_directory_atom.py\n# Log Level: INFO\n
import os
from app.atoms.base_atom import BaseAtom

class CreateDirectoryAtom(BaseAtom):
    def __init__(self):
        super().__init__('CreateDirectoryAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        os.makedirs(dir_name, exist_ok=True)
        logging.info(f'Directory \"{dir_name}\" created or already exists.')
        
        data['status'] = f'Directory \"{dir_name}\" ensured.'
        return data
"
create_file_with_content "$BASE_DIR/app/atoms/create_directory_atom.py" "$create_directory_atom_content"

# CreateFileAtom class
create_file_atom_content="# Filename: create_file_atom.py\n# Path: $BASE_DIR/app/atoms/create_file_atom.py\n# Log Level: INFO\n
import os
from app.atoms.base_atom import BaseAtom

class CreateFileAtom(BaseAtom):
    def __init__(self):
        super().__init__('CreateFileAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name', '.')
        file_name = data.get('file_name')
        content = data.get('content', '')

        if not file_name:
            raise ValueError('File name is required.')
        
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        
        logging.info(f'File \"{file_name}\" created in directory \"{dir_name}\".')
        
        data['status'] = f'File \"{file_name}\" created.'
        return data
"
create_file_with_content "$BASE_DIR/app/atoms/create_file_atom.py" "$create_file_atom_content"

# Molecule base class and SequentialMolecule
base_molecule_content="# Filename: base_molecule.py\n# Path: $BASE_DIR/app/molecules/base_molecule.py\n# Log Level: INFO\n
from abc import ABC, abstractmethod

class Molecule(ABC):
    def __init__(self):
        self.atoms = []

    def add_atom(self, atom):
        self.atoms.append(atom)

    @abstractmethod
    def run(self, data: dict):
        pass

class SequentialMolecule(Molecule):
    def run(self, data: dict) -> dict:
        for atom in self.atoms:
            data = atom.execute(data)
            if data is None:
                break
        return data
"
create_file_with_content "$BASE_DIR/app/molecules/base_molecule.py" "$base_molecule_content"

# Main entry point to execute the molecule
main_content="# Filename: main.py\n# Path: $BASE_DIR/app/main.py\n# Log Level: INFO\n
import logging
from app.atoms.create_directory_atom import CreateDirectoryAtom
from app.atoms.create_file_atom import CreateFileAtom
from app.molecules.base_molecule import SequentialMolecule

def main():
    data = {
        'dir_name': 'output',
        'file_name': 'example.txt',
        'content': 'Hello, World!'
    }

    molecule = SequentialMolecule()
    molecule.add_atom(CreateDirectoryAtom())
    molecule.add_atom(CreateFileAtom())

    try:
        result = molecule.run(data)
        print(result['status'])
    except Exception as e:
        print(f'Execution failed: {e}')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
"
create_file_with_content "$BASE_DIR/app/main.py" "$main_content"

# Unit tests for atoms and molecules
test_atoms_content="# Filename: test_atoms.py\n# Path: $BASE_DIR/tests/test_atoms.py\n# Log Level: INFO\n
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
        self.assertEqual(result['status'], \"Directory 'test_dir' ensured.\")
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
"
create_file_with_content "$BASE_DIR/tests/test_atoms.py" "$test_atoms_content"

test_molecules_content="# Filename: test_molecules.py\n# Path: $BASE_DIR/tests/test_molecules.py\n# Log Level: INFO\n
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
"
create_file_with_content "$BASE_DIR/tests/test_molecules.py" "$test_molecules_content"

# .gitignore file
gitignore_content="*.pyc\n__pycache__/\nlogs/"
create_file_with_content "$BASE_DIR/.gitignore" "$gitignore_content"

# README.md
readme_content="# Project README\n\nThis project implements a basic framework using atoms and molecules."
create_file_with_content "$BASE_DIR/README.md" "$readme_content"

requirements_content="pytest\nlogging\n"
create_file_with_content "$BASE_DIR/requirements.txt" "$requirements_content"

# setup.py for package distribution
setup_content="# Filename: setup.py\n# Path: $BASE_DIR/setup.py\n# Log Level: INFO\n
from setuptools import setup, find_packages

setup(
    name='framework',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'run_app = app.main:main',
        ],
    },
)
"
create_file_with_content "$BASE_DIR/setup.py" "$setup_content"

echo "Project structure setup completed."
