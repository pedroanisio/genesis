import logging
from app.atoms.base_atom import BaseAtom

class StateKeyAtom(BaseAtom):
    """
    Atom to set the state key for a file based on its full file path or another specified value.
    """
    
    def __init__(self):
        super().__init__("StateKeyAtom")

    def process(self, data: dict) -> dict:
        """
        Retrieves the state key from the data dictionary and ensures a valid key is provided.
        
        Args:
            data (dict): Dictionary containing 'state_key' which acts as the key to retrieve the value.
            
        Returns:
            dict: Updated dictionary with 'state_key' set to the retrieved value.
        """
        # Get the key that will be used to retrieve the value
        state_key = data.get('state_key')
        
        if not state_key:
            logging.error("No 'state_key' provided in the data dictionary.")
            raise ValueError("The 'state_key' must be provided in the data dictionary.")
        
        # Retrieve the value using the state_key as the key
        value = data.get(state_key)
        
        if not value:
            logging.error(f"No value found for state_key [{state_key}].")
            raise ValueError(f"No value found for the provided state_key: {state_key}.")

        # Set the state key to the retrieved value
        data['state_key'] = value
        logging.info(f"State key successfully set to: {state_key}")
        
        return data
