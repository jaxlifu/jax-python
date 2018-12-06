# -*- coding=utf-8 -*-
#!/usr/bin/env python

import tkinter
from tkinter.constants import *
import os


def ls():
    os.system("dir")


def pwd():
    os.system("pwd")


def main():
    tk = tkinter.Tk()
    frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH, expand=1)
    label = tkinter.Label(frame, text="Hello, World")
    label.pack(fill=X, expand=1)
    button = tkinter.Button(frame, text="ls", command=ls)
    button.pack(side=BOTTOM)
    button2 = tkinter.Button(frame, text="pwd", command=pwd)
    button2.pack(side=BOTTOM)
    tk.mainloop()


if __name__ == "__main__":
    main()
