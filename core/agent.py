class Agent:

    def __init__(self, brain, browser, system):
        self.brain = brain
        self.browser = browser
        self.system = system

    def execute(self, command):

        decision = self.brain.understand(command)

        tool = decision.get("tool")
        action = decision.get("action")
        query = decision.get("query", "")

        if tool == "browser":

            if action == "youtube":
                self.browser.youtube(query)
                return "یوتیوب باز شد."

            if action == "google":
                self.browser.google(query)
                return "گوگل باز شد."

        elif tool == "system":

            if action == "time":
                return self.system.time()

            if action == "info":
                return self.system.info()

            if action == "exit":
                return "EXIT"

        return "دستور را متوجه نشدم."
