from urllib.parse import unquote
import random

class ExitStrategy:

    def __init__(self):
        self.name = "Exit"

    def apply(self, answer, visited_pages, titles):
        new_answer = answer
        return new_answer
    
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

    @staticmethod
    def default():
        exit_strategy = ExitStrategy()
        return exit_strategy

    @staticmethod
    def standard():
        exit_strategy = StandardExitStrategy()
        return exit_strategy
    
class StandardExitStrategy(ExitStrategy):

    def apply(self, answer, visited_pages, titles):
        if (visited_pages.__contains__(answer)):
                title_list = self.create_title_list(titles, visited_pages)
                answer = "https://en.wikipedia.org/wiki/" + self.select_random(titles)
        return answer
