"""
2023-bt-raffael-rot
19-607-928
Prof. Dr. Simon Mayer
Danai Vachtsevanou, MSc.
"""

# Import utilities
import pandas as pd

# Import applications
from hyperbrain import manage

SPACE = 75


def Run() -> str:
    """ Starting point

    Note: Start the client.

    :return: str: Response messages
    """
    # Variables
    result = str()  # Response
    active = True  # While condition
    ui_codes = pd.read_json("data/ui_codes.json")  # Read the codes for the interface

    # Client
    while active:

        # Interface

        print(f"*" * SPACE)

        for code, message in ui_codes.items():
            print(f"{code}: {message['msg']}")  # Print the code and the related message
        print(f"x: Exit")  # Exit

        print(f"*" * SPACE)

        val_input = input("Please choose one option: ")  # User input for the ui code

        # Launch the correct application
        if val_input == "0":
            result = manage.Run()  # Application RBrain
        elif val_input == "x":
            result = "Exit programm"
            active = False  # While condition == False

        print(f"*" * SPACE)

    return result  # Return the result of one of the applications


if __name__ == '__main__':
    response = Run()
