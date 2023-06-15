from hyperbrain.objects.llm_interfaces.chatgpt_interface import ChatGPTInterface

def get_model_list():
    model_list = ["chatgpt", "gpt-4"]
    return model_list

def create_interface(name: str):
    interface = None
    if name == "chatgpt":
        interface = ChatGPTInterface("gpt-3.5-turbo")
    elif name == "gpt-4":
        interface = ChatGPTInterface("gpt-4")
    else:
        raise Exception("No such interface")
    return interface