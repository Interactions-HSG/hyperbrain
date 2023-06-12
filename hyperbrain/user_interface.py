"""
2023-bt-raffael-rot
19-607-928
Prof. Dr. Simon Mayer
Danai Vachtsevanou, MSc.
"""

# Import utilities
import pandas as pd


def show_ui():
    """ User interface

    Print the user interface. For this purpose, it reads the JSON file ui_codes,
    and prints the codes with the key "msg".

    """
    ui_codes = pd.read_json("hyperbrain/data/ui_codes.json")  # Read the JSON file

    # Print the user interface with the codes and given messages
    for code, message in ui_codes.items():
        print(f"{code}: {message['msg']}")
    print(f"x: Exit")

    return 0