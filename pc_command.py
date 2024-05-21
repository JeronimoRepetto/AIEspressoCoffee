from subprocess import call

class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website):
        website = "" if website is None else website
        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + website)