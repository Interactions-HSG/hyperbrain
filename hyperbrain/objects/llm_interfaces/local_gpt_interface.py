
import time
from gpt4all import GPT4All


from hyperbrain.objects.llm_interface import LLMInterface



class LocalGPTInterface(LLMInterface):
   
    def __init__(self, model_name: str = "Snoozy") -> None: 
       """ Constructor
       """
       file_name = "GPT4All-13B-snoozy.ggmlv3.q4_0.bin"
       if (model_name == "hermes"):
           file_name = "nous-hermes-13b.ggmlv3.q4_0.bin"
       self.model = GPT4All(file_name)
       
    def _ask(self, params: dict) -> str:
        """
        :params params: Contains the parameters.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        content = params["query"]
        self._set_logs("Query: " + content)
        role = params.get("role", "user")
        message = {"role": role, "content": content}
        messages = [message]
        ret = self.model.chat_completion(messages)
        print(ret)
        
        
        
        result = ret['choices'][0]['message']['content']

        time.sleep(3)
        #response = requests.post(self.API_URL, headers=headers, data=json.dumps(data))  # POST request to the OpenAi API

        #data = response.json()  # Get the JSON data from the response

        #print("data received: ", data)

        #result = data['choices'][0]['message']['content']  # Init the result of the request

        log_entry = f"The request for the question was executed successfully."  # Init a log entry

        self._set_logs(log_entry)  # Write a log entry
        
        return result  # Return result