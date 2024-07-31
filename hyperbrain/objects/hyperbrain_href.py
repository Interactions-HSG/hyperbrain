"""
2023-bt-raffael-rot
19-607-928
Prof. Dr. Simon Mayer
Danai Vachtsevanou, MSc.
"""

# Import utilities
import json
import requests
from urllib.parse import unquote
import datetime
from bs4 import BeautifulSoup
import re
import random

from hyperbrain.objects.llm_interface_creation import create_interface

from hyperbrain.objects.hyperbrain_common import HyperBrainCommon

from hyperbrain.objects.exit_strategy import ExitStrategy


class HyperBrainHref(HyperBrainCommon):
    """
    This is HyperBrain. It enables Hypermedia Guidance.
    """

    def __init__(self, model = "gpt-4", log_policy = 0) -> None:
        """ Constructor
        """
        super().__init__(model, log_policy, content ="You are a helpful system to find the most likely related keyword based on the given list." )
        self.exit_strategy = ExitStrategy.default()

    def set_exit_strategy(self, exit_strategy):
        self.exit_strategy = exit_strategy
        
        
 

    

    
    def _get_hypermedia_data(self, url: str, log_policy = 0) -> list:
        """ GET Request
        This method requests the html/text data of the Hypermedia. It extracts the hypermedia references.
        :param url: URL
        :return: List of links
        """

        response = requests.get(url)  # GET request

        html_doc = BeautifulSoup(response.content, 'html.parser')  # Transforming context into bs4

        hrefs = []  # Init an empty array for the hypermedia links
        titles = []

        for paragraph in html_doc.find_all('p'):
            # Get all hypermedia references
            for link in paragraph.find_all('a'):

                if link.get("title"):
                    hrefs.append(link.get('href'))
                    titles.append(link.get("title"))

        log_entry = f"The context of hypermedia environtment '{url}' " \
                    f"was successfully downloaded and extracted."  # Init a new log entry

        #HyperBrainHref._set_logs(log_entry, log_policy)  # Write a new log entry
        self.logger.log(log_entry, log_policy)

        return hrefs, titles

    def _ask(self, query, temperature=0.9):
        """
        :param query: Query is the input for the LLM.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        params = {"content":"You are a helpful system to find the most likely related keyword based on the given list.",
                  "query": query,
                  temperature: temperature
                  }
        result = self.llm._ask(params)
        
        return result  # Return result
        

    def hyperbrain(self, keyword: str, entry_point: str) -> str:
        """
        :param keyword: High-level goal
        :param entry_point: Starting resource of an API «Root Resource»
        :return: Return the URI of the high-level goal.
        """

        #self._set_logs(f"{10 * '*'}\nStart HyperBrain for {keyword}", self.log_policy)  # Start
        self.logger.log(f"{10 * '*'}\nStart HyperBrain for {keyword}",0)

        potential_pages = set()
        visited_pages = set()

        not_found = True  # Condition for the while loop

        while not_found:  # Search until HyperBrain finds the answer

            # Query to check if the entry point is the right hypermedia link

            query = f"Available link: '{entry_point}'\n" \
                    f"Guess if the available link is the hypermedia reference for {keyword}. Return with TRUE/FALSE."

            answer = self._ask(query)  # Get an answer‚

            #self._set_logs(f"Answer: {answer}", self.log_policy)  # Write a log entry
            self.logger.log(f"Answer: {answer}",0)

            # If True, the final application state is found
            if "TRUE" in answer:
                not_found = False

            else:  # If he does not find the answer, he shows the most related link to the topic

                hrefs, titles = self._get_hypermedia_data(entry_point, 0)  # Get hypermedia context
                potential_pages.add(entry_point)
                for t in titles:
                    potential_pages.add("https://en.wikipedia.org/wiki/"+ t)
                visited_pages.add(entry_point)
                self.logger.print("visited pages: "+str(visited_pages), 0)
                y = 200  # Number of links

                #self._set_logs(f"Available Links: {hrefs[:y]}", self.log_policy)  # Write a log entry
                self.logger.log(f"Available Links: {hrefs[:y]}",0)

                # Query 2
                query = f"List of keywords: '{titles[:y]}'. " \
                        f"Guess which of these keywords is most likely related to '{keyword}'. " \
                        f"Provide a keyword and one sentence explanation."

                answer = self._ask(query)  # Ask which link is most related

                #self._set_logs(f"Answer: {answer}", self.log_policy)  # Write a log entry
                self.logger.log(f"Answer: {answer}",0)

                # Find all links
                self.logger.print("answer: " + answer, 0)
                matches = re.findall(r'(["\'])(.*?)\1', answer)
                matches = [self.clean(match[1]) for match in matches if match[1]]
                self.logger.print("initial matches: " + str(matches), 0)
                if (len(matches) > 1 and matches.__contains__(keyword)):  # If several keywords were found, delete the high-level goal from the list
                    matches.remove(keyword)
                else:  # If there is only the high-level goal, start the next loop
                    print("Not found")
                    matches = titles
                    #continue
                self.logger.print("new matches: "+ str(matches),0)
                answer = matches[0]  # Get the first keyword from the list

                answer = "https://en.wikipedia.org/wiki/" + answer

                answer = self.exit_strategy.apply(answer, visited_pages, titles)

                #if (visited_pages.__contains__(answer)):
                 #   self.logger.print("The page has been visited", 0)
                  #  title_list = self.create_title_list(titles, visited_pages)
                   # self.logger.print("title list: "+ title_list, 0)
                    #answer = "https://en.wikipedia.org/wiki/" + self.select_random(titles)


                self.logger.print(f"Answer: {answer}", 0)

                entry_point = self.format(answer)  # Set the new url as the new local hypermedia environment

                continue

        #self._set_logs(f"End HyperBrain \n{10 * '*'}",self.log_policy)
        self.logger.log(f"End HyperBrain \n{10 * '*'}",0)

        return answer
    
    def create_title_list(self, titles: list, visited_pages: set):
        for v in visited_pages:
            if (titles.__contains__(v) and  len(titles)>1):
                titles.remove(v)
        return titles

    
    def select_random(self, titles):
        n = len(titles)
        i = random.randrange(0, n)
        return titles[i]
    
    def format(self, potential_url: str):
        url = unquote(potential_url)
        if (url[-1]== "."):
            url = url[:-1]
        return url
    
    def clean(self, keyword):
        if (keyword[-1]=="."):
            keyword = keyword[:-1]
        return keyword
        
