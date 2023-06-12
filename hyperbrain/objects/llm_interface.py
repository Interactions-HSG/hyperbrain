# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 17:31:45 2023

@author: JLemee
"""

import datetime

import hyperbrain.objects.llm_interfaces

from hyperbrain.objects.llm_interfaces.chatgpt_interface import ChatGPTInterface

class LLMInterface:
    
    def _ask(self, params: dict) -> str:
        return ""
    
    @staticmethod
    def _set_logs(log: str) -> int:
        """
        :param log: The log entry to save in the log file.
        :return: 0
        """

        now = datetime.datetime.now()  # Get the real time
        current_time = now.strftime("%H:%M:%S")  # Formatting of the date

        date_log = f"[{current_time}]  {log}\n"  # Append log entry to instance variable

        # Append a new line to the log file
        with open('hyperbrain/data/hyperbrain_logs.txt', 'a') as file:
            file.write(f"{date_log}")

        return 0
    
def create_interface(name: str):
    interface = None
    if name == "chatgpt":
        interface = ChatGPTInterface("gpt-3.5-turbo")
    elif name == "gpt4":
        interface = ChatGPTInterface("gpt-4")
    else:
        raise Exception("No such interface")
    return interface