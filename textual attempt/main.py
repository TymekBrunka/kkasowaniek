"""
Code browser example.

Run with:

    python code_browser.py PATH
"""

from __future__ import annotations

import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header, Label, Placeholder, Static
from Browser import Browser

class MyUiApp(App):
    CSS_PATH = "style.tcss"
    # SCREENS={"browser": Browser}
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    screens = {
        "browser": Browser()
    }

    def on_mount(self) -> None:
        self.install_screen(self.screens["browser"], "browser")
        # self.query_one(DirectoryTree).focus()

        def theme_change(_signal) -> None:
            """Force the syntax to use a different theme."""
            self.watch_path(None)
        self.theme_changed_signal.subscribe(self, theme_change)

    def watch_path(self, path: str | None) -> None:
        """Called when path changes."""
        code_view = self.query_one("#code", Static)
        if path is None:
            code_view.update("")
            return
        try:
            syntax = Syntax.from_path(
                path,
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark" if self.current_theme.dark else "github-light",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = path

    # def watch_path(self, path: str | None) -> None:
    #     """Called when path changes."""
    #     code_view = self.query_one("#code", Static)
    #     if path is None:
    #         code_view.update("")
    #         return
    #     try:
    #         syntax = Syntax.from_path(
    #             path,
    #             line_numbers=True,
    #             word_wrap=False,
    #             indent_guides=True,
    #             theme="github-dark" if self.current_theme.dark else "github-light",
    #         )
    #     except Exception:
    #         code_view.update(Traceback(theme="github-dark", width=None))
    #         self.sub_title = "ERROR"
    #     else:
    #         code_view.update(syntax)
    #         self.query_one("#code-view").scroll_home(animate=False)
    #         self.sub_title = path
    #
    #         self.theme_changed_signal.subscribe(self, theme_change)

if __name__ == "__main__":
    MyUiApp().run()
