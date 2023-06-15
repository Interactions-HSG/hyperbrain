"""
2023-bt-raffael-rot
19-607-928
Prof. Dr. Simon Mayer
Danai Vachtsevanou, MSc.
"""

# Import objects
from hyperbrain.objects.hyperbrain_href import HyperBrainHref
from hyperbrain.objects.hyperbrain_cherrybot import HyperBrain

# Import utilities
from hyperbrain.user_interface import show_ui

from hyperbrain.objects.llm_interface_creation import get_model_list


def hyperbrain_cherrybot(model: str) -> int:
    """ HyperBrain with input
    """
    model = HyperBrain(model)  # Initialize HyperBrain

    model.hyperbrain()  # Execute HyperBrain

    return 0


def hyperbrain_wikipedia(model: str) -> str:
    """ HyperBrain for plain hypermedia references

    :return: Hypermedia reference -> str
    """

    model = HyperBrainHref(model)  # Initialize HyperBrain

    keyword = input("Enter a keyword: ")  # Initialize high-level goal
    entry_url = input("Enter an entry url: ")  # Initialize the entry point

    result = model.hyperbrain(keyword=keyword, entry_point=entry_url)  # Execute HyperBrain

    return f"Result: {result}"


def Run() -> str:
    """ Manage HyperBrain

    Note: The Large Language Model is based on ChatGPT turbo 3.5.

    :return: str: Response messages
    """

    active = True  # While condition
    result = str()

    while active:

        show_ui()  # Show user interface

        val_input = input(f"Enter a code to be executed: ")  # User input for the code

        # Execute the right function based on the input value
        if val_input == "0":  # ChatGPT with plain hyperlinks
            model_input = input(f"Enter the model to use (models: {get_model_list()}):") 
            result = hyperbrain_wikipedia(model_input)
        elif val_input == "1":  # ChatGPT with input factors
            model_input = input(f"Enter the model to use (models: {get_model_list()}):") 
            result = hyperbrain_cherrybot(model_input)
        elif val_input == "x":  # Exit: While condition == False
            active = False
            print("Exit HyperBrain")

        print(result)

    return result

