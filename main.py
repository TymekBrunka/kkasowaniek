import pytermgui as ptg

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'

    Button:
        styles:
            label: '[@tertiary-2]{item}'
"""

with ptg.YamlLoader() as loader:
    loader.load(CONFIG)

from app import *

with ptg.WindowManager() as manager:
    window = (
        ptg.Window(
            width=60,
            box="DOUBLE"
        )
        .set_title("[210 bold]Repo")
        .center()
    )
    main_content = [
        "",
        "Wybierz repo",
        "",
        # ["Submit", lambda *_: submit(manager, window)],
        (
            ptg.Button("MOBILNE", lambda *_: app_main(window, "mobilne/JAVA 4 MOBILE", manager) ),
            ptg.Button("WEBOWE", lambda *_: app_main(window, "webowe", manager) ),
            ptg.Button("DESKTOPOWE", lambda *_: app_main(window, "desktopowe", manager) ),
            # box="EMPTY_VERTICAL"
        ),
    ]
    for i in main_content:
        window += i
    manager.add(window)
