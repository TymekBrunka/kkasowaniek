from __future__ import annotations

import sys

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header, Label, Placeholder, Static

class Browser(Screen):
    """Textual code browser app."""
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
    ]

    show_tree = var(True)
    show_code = var(True)
    path: reactive[str | None] = reactive(None)

    def watch_show_tree(self, show_tree: bool) -> None:
        self.set_class(show_tree, "-show-tree")

    def watch_show_code(self, show_code: bool) -> None:
        self.set_class(show_code, "-show-code")

    def compose(self) -> ComposeResult:
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        with Container(id="container"):
            yield DirectoryTree(path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)
        yield Footer()

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        self.path = str(event.path)

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree
