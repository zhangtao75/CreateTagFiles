
"""
Create Tag Files

Author:
Tao Zhang (zhangtao75@gmail.com)

Function:
Create tag empty files. One tag file is named after one tag you input.
These tag files are used by "everything". In this way we can attach multiple
tags onto a directory.

Python version:
Python 2.7
"""

import os
import tkinter as tk
import re

"""
This is a simplified MVC.
TagFiles:
    The Module. It do the real work but don't know anything about the View and
    the Controller.
Controller:
    The Controller. It will call the Module based on the View's change.
GUI:
    The View. It does not concern any process logic. It use a simplified
    Observer pattern, which doesn't include add_register and remove_register,
    to communicate with the Controller.
"""


class TagFiles:
    def __init__(self, path=None, tag_list=None):
        self.base_path = "C:\\"
        special_chars = "[\\/\":*?<>|]"
        self.special_re = re.compile(special_chars)
        # set path
        if path is None:
            self.path = None
        else:
            self.set_path(path)
        # set tag list
        if tag_list is None:
            self.tag_list = None
        else:
            self.set_tag(tag_list)

    def set_path(self, path):
        # if (path is None) or not(os.path.exists(path.decode("utf-8"))):
        if (path is None) or not (os.path.exists(path)):
            return -1
        self.path = path

    def set_tag(self, tag_list):
        # Checking: the input tag_list is not required to be a real list.
        #           However, each member of the tag_list must be a str.
        for tag in tag_list:
            if not(type(tag.encode('utf-8')) is str):
                return -1
        # Checking: if a tag item contains invalid char for filename, the tag
        #           item should be rejected.
        # Q: Why we check here but don't let the file creation raise errors?
        # A: Some "invalid" chars, e.g. "\", won't make the file creation to
        #    raise errors but create some unexpected files.
        self.tag_list = []
        for tag in tag_list:
            tag_str = tag.encode('utf-8')
            if self.special_re.search(tag_str) is None:
                self.tag_list.append(tag_str)

    def set_path_tags(self, path, tag_list):
        self.set_path(path)
        self.set_tag(tag_list)

    def create_tag_files(self):
        # check the existence of path and tag list
        if (self.path is None) or (self.tag_list is None):
            return -1
        # os.chdir(self.path.decode("utf-8"))
        os.chdir(self.path)
        res = ""
        for tag in self.tag_list:
            try:
                open(tag.decode("utf-8")+".tag", 'a').close()
                print "creating " + tag.decode("utf-8")+".tag"
            except Exception as e:
                res += (e.message + "; ")
        os.chdir(self.base_path)


class GUI:
    def __init__(self, main_controller):
        # initiate the controller
        if main_controller is None:
            exit(-1)
        self.controller = main_controller

        # main window
        self.frm_root = tk.Frame(width=285, height=210)
        self.frm_root.grid_propagate(0)
        self.frm_root.grid(padx=15, pady=15)

        # input frame
        self.frm_input = tk.Frame(self.frm_root)
        self.frm_input.grid(row=0, padx=5, pady=5)
        # tags row - label
        self.lbl_tags = tk.Label(self.frm_input, text="Tags")
        self.lbl_tags.grid(row=0, column=0, sticky=tk.NW, padx=5)
        # tags row - text input
        self.txt_tags = tk.Text(self.frm_input, width=27, height=10)
        self.txt_tags.grid(row=0, column=1, sticky=tk.E)
        # tags row - text input scroll bar
        self.srb_tags = tk.Scrollbar(self.frm_input,
                                     command=self.txt_tags.yview)
        self.txt_tags.config(yscrollcommand=self.srb_tags)
        self.srb_tags.grid(row=0, column=2, sticky=tk.W+tk.N+tk.S)
        # path row - label
        self.lbl_path = tk.Label(self.frm_input, text="Directory")
        self.lbl_path.grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        # path row - path entry
        self.etr_path = tk.Entry(self.frm_input, width=30)
        self.etr_path.grid(row=1, column=1, columnspan=2, pady=5)

        # button frame
        self.frm_button = tk.Frame(self.frm_root)
        self.frm_button.grid(row=1, ipadx=5, ipady=5)
        # create button
        self.btn_create = tk.Button(self.frm_button, text='Create', width=5)
        self.btn_create.grid(row=0, column=0, sticky=tk.W, padx=30)
        self.btn_create.config(command=self.create_button_click)
        # close button
        self.btn_close = tk.Button(self.frm_button, text='Close', width=5)
        self.btn_close.grid(row=0, column=1, sticky=tk.E, padx=30)
        self.btn_close.config(command=self.close_button_click)

    def close_button_click(self):
        self.controller.event_raised("close", self)

    def create_button_click(self):
        self.controller.event_raised("create", self)

    def get_path(self):
        return self.etr_path.get()

    def get_tags(self):
        return self.txt_tags.get('1.0', tk.END)

    def quit(self):
        self.frm_root.quit()

    def mainloop(self):
        self.frm_root.mainloop()


class Controller:
    def __init__(self, module):
        self.process_module = module

    def event_raised(self, event_type, view):
        if event_type == "close":
            view.quit()
        if event_type == "create":
            path = view.get_path()
            tag_list = view.get_tags().split()
            self.process_module.set_path_tags(path, tag_list)
            self.process_module.create_tag_files()

if __name__ == '__main__':
    process_module = TagFiles()
    controller = Controller(process_module)
    mainProgram = GUI(controller)
    mainProgram.mainloop()
