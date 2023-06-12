# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:40:44 2023

@author: JLemee
"""

class ChatGPTInterface:
   
    def __init__(self) -> None:
       """ Constructor
       """
       # Get the API KEY from a secure .txt file
       with open('hyperbrain/data/API_KEY.txt', 'r') as f:
           self.API_KEY = f.read()
       self.API_URL = "https://api.openai.com/v1/chat/completions"  # API URL from OpenAI
       
       
    def _ask(self, content: str, query: str, model="gpt-4", temperature=0.9) -> str:
        """
        :param query: Query is the input for the LLM.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        # Init the headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key_chat_gpt}"
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

        time.sleep(3)
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))  # POST request to the OpenAi API

        data = response.json()  # Get the JSON data from the response

        result = data['choices'][0]['message']['content']  # Init the result of the request

        return result  # Return result