# Filename: base_atom.py\n# Path: project_root/app/atoms/base_atom.py\n# Log Level: INFO\n
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
            logging.error(f'Error in atom "{self.name}": {e}')
            raise RuntimeError(f'Failed to execute atom "{self.name}"')

    @abstractmethod
    def process(self, data: dict) -> dict:
        pass

