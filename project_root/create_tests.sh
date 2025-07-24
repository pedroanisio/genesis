#!/bin/bash

# Define base directory
BASE_DIR="/home/pals/code/_temp/genesis/project_root"

# Create directories
declare -a DIRS=(
    "$BASE_DIR/app/atoms",
    "$BASE_DIR/tests"
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

# Atoms and their respective test files

# CreateDirectoryAtom
create_directory_atom_content="""
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
        data['status'] = f'Directory "{dir_name}" ensured.'
        return data
"""
create_file_with_content "$BASE_DIR/app/atoms/create_directory_atom.py" "$create_directory_atom_content"

test_create_directory_atom_content="""
import unittest
import os
from app.atoms.create_directory_atom import CreateDirectoryAtom

class TestCreateDirectoryAtom(unittest.TestCase):
    def test_process(self):
        atom = CreateDirectoryAtom()
        data = {'dir_name': 'test_dir'}
        result = atom.process(data)
        self.assertTrue(os.path.exists('test_dir'))
        self.assertEqual(result['status'], "Directory 'test_dir' ensured.")
        os.rmdir('test_dir')

if __name__ == '__main__':
    unittest.main()
"""
create_file_with_content "$BASE_DIR/tests/test_create_directory_atom.py" "$test_create_directory_atom_content"

# CreateFileAtom
create_file_atom_content="""
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
        
        data['status'] = f'File "{file_name}" created.'
        return data
"""
create_file_with_content "$BASE_DIR/app/atoms/create_file_atom.py" "$create_file_atom_content"

test_create_file_atom_content="""
import unittest
import os
from app.atoms.create_file_atom import CreateFileAtom

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

if __name__ == '__main__':
    unittest.main()
"""
create_file_with_content "$BASE_DIR/tests/test_create_file_atom.py" "$test_create_file_atom_content"

# DeleteFileAtom
delete_file_atom_content="""
import os
from app.atoms.base_atom import BaseAtom

class DeleteFileAtom(BaseAtom):
    def __init__(self):
        super().__init__('DeleteFileAtom')

    def process(self, data: dict) -> dict:
        file_path = data.get('file_path')

        if not file_path:
            raise ValueError('No file path provided for deletion.')

        if os.path.exists(file_path):
            os.remove(file_path)
            data['file_deleted'] = True
        else:
            data['file_deleted'] = False
        
        return data
"""
create_file_with_content "$BASE_DIR/app/atoms/delete_file_atom.py" "$delete_file_atom_content"

test_delete_file_atom_content="""
import unittest
import os
from app.atoms.delete_file_atom import DeleteFileAtom

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
        os.rmdir('test_dir')

if __name__ == '__main__':
    unittest.main()
"""
create_file_with_content "$BASE_DIR/tests/test_delete_file_atom.py" "$test_delete_file_atom_content"

# ListMkvFilesAtom
list_mkv_files_atom_content="""
import os
from app.atoms.base_atom import BaseAtom

class ListMkvFilesAtom(BaseAtom):
    def __init__(self):
        super().__init__('ListMkvFilesAtom')

    def process(self, data: dict) -> dict:
        dir_name = data.get('dir_name')
        if not dir_name:
            raise ValueError('Directory name is required.')
        
        mkv_files = []
        for root, dirs, files in os.walk(dir_name):
            for file_name in files:
                if file_name.endswith('.mkv'):
                    mkv_files.append({'filename': file_name, 'path': os.path.join(root, file_name)})
        
        data['items'] = mkv_files
        return data
"""
create_file_with_content "$BASE_DIR/app/atoms/list_mkv_files_atom.py" "$list_mkv_files_atom_content"

test_list_mkv_files_atom_content="""
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
"""
create_file_with_content "$BASE_DIR/tests/test_list_mkv_files_atom.py" "$test_list_mkv_files_atom_content"

# SortBySizeAtom
sort_by_size_atom_content="""
from app.atoms.base_atom import BaseAtom

class SortBySizeAtom(BaseAtom):
    def __init__(self):
        super().__init__('SortBySizeAtom')

    def process(self, data: dict) -> dict:
        items = data.get('items', [])
        sorted_items = sorted(items, key=lambda x: x.get('size', 0), reverse=True)
        data['sorted_items'] = sorted_items
        return data
"""
create_file_with_content "$BASE_DIR/app/atoms/sort_by_size_atom.py" "$sort_by_size_atom_content"

test_sort_by_size_atom_content="""
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
"""
create_file_with_content "$BASE_DIR/tests/test_sort_by_size_atom.py" "$test_sort_by_size_atom_content"

# More atoms and their tests can be added here similarly...

# Final message
echo "All atoms and their respective test files have been created successfully."

