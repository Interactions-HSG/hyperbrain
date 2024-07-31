
from hyperbrain.objects.logger import Logger

from hyperbrain.objects.llm_interface_creation import create_interface

class HyperBrainCommon:

    def __init__(self,model , log_policy, content: str):
        self.logger = Logger(log_policy)
        self.llm = create_interface(model)
        self.content = content

    def _ask(self, query, temperature=0.9):
        """
        :param query: Query is the input for the LLM.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        params = {"content": self.content,
                  "query": query,
                  temperature: temperature
                  }
        result = self.llm._ask(params)
        
        return result  # Return result
    
    