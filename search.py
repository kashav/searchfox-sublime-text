import sublime, sublime_plugin
import webbrowser

CHECKOUT = "mozilla-central"  # maybe make this configurable?
BASE = "https://searchfox.org/" + CHECKOUT

PATH_MARKER = "@"
REGEXP_MARKER = "rrr"

SELECTION = 1
PATH = 2
QUERY = 3


def get_url(text, t):
    if t == SELECTION:
        return "{}/search?q={}".format(BASE, text)

    if t == PATH:
        return "{}/source/{}".format(BASE, text)

    if t == QUERY:
        q, _, path = text.partition(PATH_MARKER)

        regexp = q.startswith(REGEXP_MARKER)
        if regexp:
            q = q.split(REGEXP_MARKER).pop()

        url = "{}/search?q={}&path={}".format(BASE, q.strip(), path.strip())
        if regexp:
            url += "&regexp=true"

        return url


def open_search_tab(text, t):
    webbrowser.open(get_url(text, t), new=2, autoraise=True)


class SearchfoxSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in self.view.sel():
            if not sel.empty():
                open_search_tab(self.view.substr(sel), SELECTION)


class SearchfoxPathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        path = self.view.file_name().split(CHECKOUT).pop()

        row = 0
        for sel in self.view.sel():
            row, _ = self.view.rowcol(sel.begin())
            break

        if row != 0:
            path += "#" + str(row)

        open_search_tab(path, PATH)


class SearchfoxQueryCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Search %s:" % CHECKOUT, "", self._on_done, self._on_change, self._on_cancel
        )

    def _on_done(self, input):
        open_search_tab(input, QUERY)

    def _on_change(self, input):
        pass

    def _on_cancel(self, input):
        pass
