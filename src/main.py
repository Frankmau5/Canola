#!/usr/bin/env python3
from platform import system
import gtk3_gui

def on_close(self, d):
    pass


def main():
    """Starting point of program\n
    Loads UI for os the program running on\n
    NOTE: Windows will be not be using the GTK3 UI"""
    if system() == "Linux":
        app = gtk3_gui.App()
        try:
            app.run()
            if app.need_to_save:
                app.backend.db_utils.write_db(app.database)
        except KeyboardInterrupt:
            if app.need_to_save:
                app.backend.db_utils.write_db(app.database)
    else:
        print("windows")


if __name__ == "__main__":
    main()
