from __future__ import annotations

from asyncio import sleep

from textual import events, on
from textual.app import App, ComposeResult

from textual.containers import Center, Container, VerticalScroll, Horizontal, Vertical
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, Placeholder, Static, Button

import sys
from os import listdir
from os.path import isdir

#--screen classes
class RepoChooser(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="container"):
            with Vertical():
                yield Static("Wybierz repo", classes="title")
                with Horizontal(classes="centerify"):
                    yield Button("mobilne", id="rp-mobilne", classes=" repo mobilne")
                    yield Button("webowe", id="rp-webowe", classes=" repo webowe")
                    yield Button("desktopowe", id="rp-desktopowe", classes=" repo desktopowe")
        yield Footer()

class ProjectsPreview(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="container"):
            with Vertical():
                yield Static("repo: .", id="repo-title", classes="title")
                with Vertical(id="folders", classes="centerify"):
                    pass
        yield Footer()
#--screen classes

class Ui(App):
    CSS_PATH = "style.tcss"
    # SCREENS={"browser": Browser}
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    MODES = {
        "repo": RepoChooser,
        "preview": ProjectsPreview,
    }

    path: var[str] = var("")
    repo: var[str | None] = var(None)

    def on_mount(self) -> None:
        path = "./" if len(sys.argv) < 1 else sys.argv[0]
        self.theme = "gruvbox"
        self.switch_mode("repo")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.classes != None:
            if "repo" in event.button.classes:
                assert event.button.id is not None
                self.repo = event.button.id[3:]
                self.path += "repo-" + self.repo
                await self.switch_mode("preview")
                self.query_one("#repo-title", Static).update(f"repo: {self.repo}")
                for i in listdir(self.path):
                    if isdir(i):
                        pass

if __name__ == "__main__":
    print(Ui().run())
