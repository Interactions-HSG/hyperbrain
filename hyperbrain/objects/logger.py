import datetime

class Logger:

    def __init__(self, policy: int = 0, log_file : str = 'hyperbrain/data/hyperbrain_logs.txt'):
        self.policy = policy
        self.log_file = log_file
        #policy = 0 means no log and only error prints.
        #Levels: fatal, error, warn, info, debug, trace

    def log(self, log: str, priority: int = 0):
        if (self.visibility(priority)):
            now = datetime.datetime.now()  # Get the real time
            current_time = now.strftime("%H:%M:%S")  # Formatting of the date

            date_log = f"[{current_time}]  {log}\n"  # Append log entry to instance variable
            date_log = self.update_date_log(date_log)
            # Append a new line to the log file
            with open(self.log_file, 'a') as file:
                file.write(f"{date_log}")

    def update_date_log(self, date_log):
        new_date_log = date_log
        n = len(date_log)
        for i in range(n):
            c = date_log[i]
            if c == '\u02bb':
                print("troublesome character u02bb detected")
                new_date_log[i]="'"
        return new_date_log

    def print(self, log:str, priority: int = 0):
        if (self.visibility(priority)):
            print(log)

    def visibility(self, priority):
        b = False
        if (priority>=5-self.policy):
            b = True
        return b


    

