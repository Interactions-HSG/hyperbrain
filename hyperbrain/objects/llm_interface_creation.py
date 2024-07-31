from hyperbrain.objects.llm_interfaces.chatgpt_interface import ChatGPTInterface
from hyperbrain.objects.llm_interfaces.local_gpt_interface import LocalGPTInterface

def get_model_list():
    model_list = ["chatgpt", "gpt-4", "Snoozy", "Hermes"]
    return model_list

def create_interface(name: str):
    interface = None
    if name == "chatgpt":
        interface = ChatGPTInterface("gpt-3.5-turbo")
    elif name == "gpt-4":
        interface = ChatGPTInterface("gpt-4")
    elif name == "Snoozy":
        interface = LocalGPTInterface("Snoozy")
    elif name == "Hermes":
        interface = LocalGPTInterface("Hermes")
    else:
        raise Exception("No such interface")
    return interface