import webbrowser
from urllib.parse import quote


class BrowserTool:

    def youtube(self, query):
        search = quote(query)
        url = f"https://www.youtube.com/results?search_query={search}"
        webbrowser.open(url)

    def google(self, query):
        search = quote(query)
        url = f"https://www.google.com/search?q={search}"
        webbrowser.open(url)
