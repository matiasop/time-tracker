import subprocess
import time
import json
import re

class TimeTracker:
    def __init__(self):
        self.time_interval = 30 # seconds between getting current window name
        self.filename = "/home/movalle/Desktop/timetracker.log" # filename with all the active window names
        self.json_results = "/home/movalle/Desktop/timetracker.json"  # filename with the analysis of the logfile
        self.counter = 0 # Number of lines written without cleaning the logfile
        self.max_counter = 10 # Maximum number of lines before the logfile is cleaned
        self.data = {} # Dictionary with the results of the analysis
        # List of common programs
        self.regex_match = re.compile(r"- Code -|- Mousepad|— Mozilla Firefox|Terminal -|- File Manager|Zoom")

    def get_window_name(self):
        # Get active window name
        ps = subprocess.Popen(["xdotool", "getactivewindow", "getwindowname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = ps.communicate()
        return output.decode("utf-8").strip()

    def cleanup(self, window_name):
        # Remove unnecesary information from window_name string
        match = re.search(self.regex_match, window_name)
        if match:
            window_name = window_name[match.start():match.end()].replace("-", "").replace("—", "").strip()
        print(window_name)
        return window_name

    def write_window_name(self):
        # Writes the window name on logfile
        window_name = self.get_window_name()
        window_name = self.cleanup(window_name)
        with open(self.filename, "a") as logfile:
            logfile.write(window_name + "\n")

    def analysis(self):
        # Reads the logfile and makes a json of a dictionary with the time logs
        with open(self.json_results, "r") as json_file:
            try:
                self.data = json.load(json_file)
            except TypeError:
                print("Error while reading JSON file")

        # Update data dictionary with the contents of the logfile
        with open(self.filename, "r") as logfile:
            lines = logfile.readlines()
            for line in lines:
                line = line.strip()
                if line in self.data:
                    self.data[line] += self.time_interval
                else:
                    self.data[line] = self.time_interval

        # Write data to JSON file
        with open(self.json_results, "w") as json_file:
            json.dump(self.data, json_file)

        # Erase the contents of the logfile
        with open(self.filename, "w") as logfile:
            pass

    def run_tracker(self):
        # Writes the name of the active window every [time_interval] seconds
        while True:
            self.write_window_name()
            time.sleep(self.time_interval)
            self.counter += 1
            if self.counter == self.max_counter:
                self.counter = 0
                self.analysis()

if __name__ == "__main__":
   tracker = TimeTracker()
#    tracker.analysis()
   tracker.run_tracker()
    