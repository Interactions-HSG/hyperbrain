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


class HyperBrainHref:
    """
    This is HyperBrain. It enables Hypermedia Guidance.
    """

    def __init__(self, model = "gpt-4") -> None:
        """ Constructor
        """
        # Get the API KEY from a secure .txt file
        self.llm = create_interface(model) # API URL from OpenAI
 

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

    @staticmethod
    def _get_hypermedia_data(url: str) -> list:
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

        HyperBrainHref._set_logs(log_entry)  # Write a new log entry

        return hrefs, titles

    def _ask(self, query, model="gpt-3.5-turbo", temperature=0.9):
        """
        :param query: Query is the input for the LLM.
        :param model: Select the LLM model from OpenAI.
        :param temperature: Hyperparameter of the LLM to set the randomness.
        :return: Return the response of the LLM.
        """
        params = {"content":"You are a helpful system to find the most likely related keyword based on the given list.",
                  "query": query,
                  "model": model,
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

        self._set_logs(log=f"{10 * '*'}\nStart HyperBrain for {keyword}")  # Start

        potential_pages = set()
        visited_pages = set()

        not_found = True  # Condition for the while loop

        while not_found:  # Search until HyperBrain finds the answer

            # Query to check if the entry point is the right hypermedia link

            query = f"Available link: '{entry_point}'\n" \
                    f"Guess if the available link is the hypermedia reference for {keyword}. Return with TRUE/FALSE."

            answer = self._ask(query)  # Get an answer‚

            self._set_logs(log=f"Answer: {answer}")  # Write a log entry

            # If True, the final application state is found
            if "TRUE" in answer:
                not_found = False

            else:  # If he does not find the answer, he shows the most related link to the topic

                hrefs, titles = self._get_hypermedia_data(entry_point)  # Get hypermedia context
                potential_pages.add(entry_point)
                for t in titles:
                    potential_pages.add("https://en.wikipedia.org/wiki/"+ t)
                visited_pages.add(entry_point)
                print("visited pages: ", visited_pages)
                y = 200  # Number of links

                self._set_logs(log=f"Available Links: {hrefs[:y]}")  # Write a log entry

                # Query 2
                query = f"List of keywords: '{titles[:y]}'. " \
                        f"Guess which of these keywords is most likely related to '{keyword}'. " \
                        f"Provide a keyword and one sentence explanation."

                answer = self._ask(query)  # Ask which link is most related

                self._set_logs(log=f"Answer: {answer}")  # Write a log entry

                # Find all links
                print("answer: ", answer)
                matches = re.findall(r'(["\'])(.*?)\1', answer)
                matches = [match[1] for match in matches if match[1]]
                print("initial matches: ", matches)
                if len(matches) > 1:  # If several keywords were found, delete the high-level goal from the list
                    matches.remove(keyword)
                else:  # If there is only the high-level goal, start the next loop
                    print("Not found")
                    continue
                print("new matches: ", matches)
                answer = matches[0]  # Get the first keyword from the list

                answer = "https://en.wikipedia.org/wiki/" + answer

                if (visited_pages.__contains__(answer)):
                    print("The page has been visited")
                    title_list = self.create_title_list(titles, visited_pages)
                    print("title list: ", title_list)
                    answer = "https://en.wikipedia.org/wiki/" + self.select_random(titles)

                

                print(f"Answer: {answer}")

                entry_point = self.format(answer)  # Set the new url as the new local hypermedia environment

                continue

        self._set_logs(f"End HyperBrain \n{10 * '*'}")

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
            print("new url: ", url)
        return url
        
