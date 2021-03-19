#!/usr/bin/env python3
from platform import system
import gtk3_gui

def main():
    """Starting point of program\n
    Loads UI for os the program running on\n
    NOTE: Windows will be not be using the GTK3 UI"""
    if system() == "Linux":
       app = gtk3_gui.App()
       app.run()
        
    else:
        print("windows")


if __name__ == "__main__":
    main()
