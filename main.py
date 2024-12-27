from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Header, Label, Static, Button

import sys
from app import Finder

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
        self.path = "../" if len(sys.argv) < 2 else sys.argv[1]
        self.theme = "nord"
        self.switch_mode("repo") #switching page

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.classes != None:
            if "repo" in event.button.classes:

                """checking if button has repo class"""
                assert event.button.id is not None
                self.repo = event.button.id[3:]
                self.path += "repo-" + self.repo
                await self.switch_mode("preview")
                self.query_one("#repo-title", Static).update(f"repo: {self.repo}")

                """Listing all folders"""
                folders_list_widget : Vertical = self.query_one("#folders", Vertical)
                for i in Finder.get_all_projects(self.path, self.repo):
                    folders_list_widget.mount(
                        #print only the folder name of project ( last element of i[1] splitted by /) and if it is compressed or not
                        Button(f"{i[1].split('/')[-1]} {'(zip)' if i[2] else ''}" )
                    )

if __name__ == "__main__":
    Ui().run()
