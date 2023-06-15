# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:40:44 2023

@author: JLemee

"""

import time

import requests

import json

from hyperbrain.objects.llm_interface import LLMInterface

class ChatGPTInterface(LLMInterface):
   
    def __init__(self, model = "gpt-4") -> None:
       """ Constructor
       """
       # Get the API KEY from a secure .txt file
       with open('hyperbrain/data/API_KEY.txt', 'r') as f:
           self.API_KEY = f.read()
       self.API_URL = "https://api.openai.com/v1/chat/completions"  # API URL from OpenAI
       self.model = model
       
    def _ask(self, params: dict) -> str:
        """
        :params params: Contains the parameters.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        content = params["content"]
        query = params["query"]
        model = params.get("model", self.model)
        temperature = params.get("temperature", 0.9)
        # Init the headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.API_KEY}"
        }

        # Init the data for the request
        data = {
            "model": model,
            "messages":
                [
                    {
                        "role": "system",
                        "content": content
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
            "temperature": temperature
        }
        self._set_logs("Query: " + query)

        time.sleep(3)
        response = requests.post(self.API_URL, headers=headers, data=json.dumps(data))  # POST request to the OpenAi API

        data = response.json()  # Get the JSON data from the response

        result = data['choices'][0]['message']['content']  # Init the result of the request

        log_entry = f"The request for the question was executed successfully."  # Init a log entry

        self._set_logs(log_entry)  # Write a log entry
        
        return result  # Return result