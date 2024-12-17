import pytermgui as ptg
from os import chdir, listdir
from os.path import isdir
def app_main(old: ptg.Window, type: str, manager: ptg.manager.WindowManager):
    manager.remove(old)
    try:
        chdir(f"../repo-{type}")
    except Exception as err:
        print(f"Wystąpił błąd: {err}")
    win = (
        ptg.Window(
            width=60,
            box="DOUBLE"
        )
        .set_title("[210 bold]kk kasowanie")
        .center()
    )

    dir_view = ptg.Container(
        box="EMPTY_VERTICAL"
    )

    for i in listdir("."):
        if isdir(i):
            dir_view += ptg.Button(i) 

    win += dir_view
    manager.add(win)
