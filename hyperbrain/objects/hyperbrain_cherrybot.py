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

API_URL = "https://api.openai.com/v1/chat/completions"  # Get the API URL of a model from ChatGPT


class HyperBrain:
    """
    """
    def __init__(self, model = "gpt-4", log_policy=0):
        """
        """
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
    def _set_logs(log: str, policy=0) -> int:
        """
        :param log: The log entry to save in the log file.
        :return: 0
        """
        if (policy !=0):
            now = datetime.datetime.now()  # Get the real time
            current_time = now.strftime("%H:%M:%S")  # Formatting of the date

            date_log = f"[{current_time}]  {log}\n"  # Append log entry to instance variable

            # Append a new line to the log file
            with open('hyperbrain/data/hyperbrain_cherrybot_logs.txt', 'a') as file:
                file.write(f"{date_log}")

        return 0

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

    def _ask(self, query: str, temperature=0.9) -> str:
        """
        :param query: Query is the input for the LLM.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        params = {"content":"You are a helpful system to give instruction to interact with an API.",
                  "query": query,
                  temperature: temperature
                  }
        #print("params: ", params)
        result = self.llm._ask(params)
        
        return result  # Return result

    def _thinking(self, action: str) -> int:
        """
        :param action: Instructions to interact with the robotic arm.
        :return: The method returns the status code from the request of the executed Python code.
        """

        query = f"Description '{self._description}'. Memory '{self._memory}'. Action '{action}'. " \
                f"Provide instructions in Python to process the action independently. " \
                f"Process the JSON file 'memory.json' with the results from the interaction." \


        self._set_logs(f"Memory: {self._memory}", self.log_policy)

        answer = self._ask(query)

        code = self._get_python_code(answer)

        self._set_logs(f"Code: {code}", self.log_policy)

        loc = {}

        time.sleep(10)

        exec(code, globals(), loc)

        self._set_logs(f"LOC: {loc}", self.log_policy)

        status_code = loc['response'].status_code

        self._set_logs(status_code, self.log_policy)

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
