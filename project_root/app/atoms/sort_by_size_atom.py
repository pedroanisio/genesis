# Filename: sort_by_size_atom.py
# Path: project_root/app/atoms/sort_by_size_atom.py
# Log Level: INFO

from app.atoms.base_sorting_atom import BaseSortingAtom

class SortBySizeAtom(BaseSortingAtom):
    """
    Atom to sort a list of dictionaries by the 'size' attribute in descending order.
    """

    def __init__(self):
        # Call the base class constructor with sort_key='size' and ascending=False
        super().__init__(name="SortBySizeAtom", sort_key="size", ascending=False)
