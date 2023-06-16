"""
2023-bt-raffael-rot
19-607-928
Prof. Dr. Simon Mayer
Danai Vachtsevanou, MSc.
"""

# Import utilities
import json
import requests
import datetime
import re
import time

from hyperbrain.objects.llm_interface_creation import create_interface

from hyperbrain.objects.hyperbrain_common import HyperBrainCommon

API_URL = "https://api.openai.com/v1/chat/completions"  # Get the API URL of a model from ChatGPT

class Memory:

    def __init__(self, file_name= 'memory.json'):
        self.file_name = file_name
        with open(file_name, 'r') as f:
            self.memory = json.load(f)  # Get memory

    def update_read(self):
        with open(self.file_name, 'r') as f:
            self.memory = json.load(f)  # Get memory

    def update_write(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.memory, f)

    def put(self, key, value):
        self.memory[key]=value
        self.update_write()

    def get(self, key):
        self.update_read()
        return self.memory[key]
    
global_memory = Memory()




class HyperBrainCherrybot(HyperBrainCommon):
    """
    """
    def __init__(self, model, log_policy, content ="You are a helpful system to give instruction to interact with an API." ):
        """
        """
        super().__init__(model, log_policy, content )
        #print("model: ", model)
        self.llm = create_interface(model)

        with open('hyperbrain/data/cherrybot_yaml.txt', 'r') as f:
            description_api = f.read()  # GET description of the API

        with open('memory.json', 'r') as f:
            memory = json.load(f)  # Get memory

        self._description = description_api  # Description of the API
        self._memory = memory  # Memory of HyperBrain
        self._high_level_goal = str()  # High-level goal
        self.log_policy = log_policy

    

    @staticmethod
    def _get_python_code(data: str) -> str:
        """
        :param data: The response of the LLM from the action ask.
        :return: Extract and return all Python code from the given string.
        """
        code_string = ""

        python_code = re.findall('```(.*?)```', data, re.DOTALL)

        for i in range(len(python_code)):
            if "python" in python_code[i]:
                temp = python_code[i]
                python_code[i] = temp[6:]

        for item in python_code:
            code_string += item

        return code_string

    def _thinking(self, action: str) -> int:
        """
        :param action: Instructions to interact with the robotic arm.
        :return: The method returns the status code from the request of the executed Python code.
        """

        query = f"Description '{self._description}'. Memory '{self._memory}'. Action '{action}'. " \
                f"Provide instructions in Python to process the action independently. " \
                f"Process the JSON file 'memory.json' with the results from the interaction." \


        #self._set_logs(f"Memory: {self._memory}", self.log_policy)
        self.logger.log(f"Memory: {self._memory}",0)

        answer = self._ask(query)

        code = self._get_python_code(answer)

        #self._set_logs(f"Code: {code}", self.log_policy)
        self.logger.log(f"Code: {code}",0)
        self.logger.print("code: "+ code, 0)

        loc = {}

        time.sleep(10)
        self.logger.print("globals"+ str(globals()), 0)

        exec(code, globals(), loc)

        #self._set_logs(f"LOC: {loc}", self.log_policy)
        self.logger.log(f"LOC: {loc}", 0)

        status_code = loc['response'].status_code

        #self._set_logs(status_code, self.log_policy)
        self.logger.log(status_code, 0)

        with open('memory.json', 'r') as f:
            memory = json.load(f)  # Get memory
            self._memory = memory

        return status_code

    def hyperbrain(self) -> int:
        """

        """
        active = True

        while active:

            action = input("Please provide an action: ")

            self._high_level_goal = action

            executed = True

            while executed:

                status_code = self._thinking(self._high_level_goal)

                if status_code == 200:

                    if action == self._high_level_goal:
                        break
                    else:
                        action = self._high_level_goal

                elif status_code == 401:
                    action = "Register an operator"
                    status_code = self._thinking(action)

                elif status_code == 403:
                    action = "Get current operator"
                    status_code = self._thinking(action)

                elif status_code == 400:
                    status_code = self._thinking(action)

                print(f"Status code: {status_code}")

            if action == "x":
                break

        return 0


def main():
    pass


if __name__ == '__main__':
    main()
