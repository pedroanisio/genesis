# Filename: base_sorting_atom.py
# Path: project_root/app/atoms/base_sorting_atom.py
# Log Level: INFO

from app.atoms.base_atom import BaseAtom
import logging

class BaseSortingAtom(BaseAtom):
    """
    BaseSortingAtom provides a generic method to sort a list of dictionaries
    based on a given attribute and order (ascending or descending).
    """

    def __init__(self, name: str, sort_key: str, ascending: bool = True):
        """
        Initialize the sorting atom.

        Args:
            name (str): Name of the atom.
            sort_key (str): The key by which to sort the dictionaries.
            ascending (bool): Whether to sort in ascending order (default: True).
        """
        super().__init__(name)
        self.sort_key = sort_key
        self.ascending = ascending

    def process(self, data: dict) -> dict:
        """
        Process the data by sorting a list of dictionaries.

        Args:
            data (dict): Data containing the list to be sorted.
            
        Returns:
            dict: Data with the sorted list.
        """
        items = data.get('items', [])
        if not items:
            raise ValueError('No items found to sort.')

        logging.info(f'Sorting {len(items)} items by "{self.sort_key}" in {"ascending" if self.ascending else "descending"} order.')

        sorted_items = sorted(items, key=lambda x: x.get(self.sort_key, 0), reverse=not self.ascending)
        data['sorted_items'] = sorted_items
        return data
