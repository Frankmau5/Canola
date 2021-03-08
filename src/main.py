#!/usr/bin/env python3
from platform import system
import gtk3_gui

def main():
    if system() == "Linux":
       app =  gtk3_gui.App()
       app.run()
        
    else:
        print("windows")


if __name__ == "__main__":
    main()
