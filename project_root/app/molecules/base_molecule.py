# Filename: base_molecule.py
# Path: project_root/app/molecules/base_molecule.py
# Log Level: INFO

from abc import ABC, abstractmethod

class Molecule(ABC):
    def __init__(self):
        self.atoms = []

    def add_atom(self, atom):
        """Add an atom to the molecule."""
        self.atoms.append(atom)

    @abstractmethod
    def run(self, data: dict):
        """Abstract method to run the molecule with a sequence of atoms."""
        pass

class SequentialMolecule(Molecule):
    """
    A molecule that executes atoms sequentially in the order they were added.
    If any atom fails or returns None, the execution halts.
    """
    def run(self, data: dict) -> dict:
        """Execute the chain of atoms sequentially."""
        for atom in self.atoms:
            data = atom.execute(data)
            if data is None:
                break
        return data
