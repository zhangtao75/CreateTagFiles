
"""
Create Tag Files

Author:
Tao Zhang (zhangtao75@gmail.com)

Function:
Create empty tag files with the names you specified.

These tag files within a directory play as tags to that directory. For example, 
you can create "Classic", "Symphony", "Hydn", "Karajan", "Berlin_Philharmonic" 
tags with that CD audio files. So when you use a desktop file-search utility, 
such as "everything", you can find all Hydn's works easily.

More explanation:
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

Python version:
Python 3.6
"""

import os
import tkinter as tk
import re

class TagFiles:
    """The module class which create specified tag files within the specified 
       directory
    """
    def __init__(self, path=None, tag_list=None):
        """initialize self._path and self._tag_list"""
        # initialize internal constants
        self.BASE_PATH = "C:\\"
        self.SPECIAL_RE = re.compile("[\\/\":*?<>|]")
        
        if path is None:
            self._path = None
        else:
            self.set_path(path)
        
        if tag_list is None:
            self._tag_list = None
        else:
            self.set_tag(tag_list)

    def set_path(self, path):
        """set self._path after checking its validity"""
        if (path is None) or not (os.path.exists(path)):
            return -1
        self._path = path

    def set_tag(self, tag_list):
        """set self._tag_list after checking the list validity"""
        for tag in tag_list:
            if type(tag) is not str:
                return -1
        # Checking: if a tag item contains invalid char for filename, the tag
        #           item should be rejected.
        # Q: Why we check here but don't let the file creation raise errors?
        # A: Some "invalid" chars, e.g. "\", won't make the file creation to
        #    raise errors but create some unexpected files.
        self._tag_list = []
        for tag in tag_list:
            # tag_str = tag.encode('utf-8')     # unnecessary in Python 3
            if self.SPECIAL_RE.search(tag) is None:
                self._tag_list.append(tag)

    def set_path_tags(self, path, tag_list):
        """initialize self._path and self._tag_list at the same time"""
        self.set_path(path)
        self.set_tag(tag_list)

    def create_tag_files(self):
        """create tag files"""
        # check the existence of path and tag list
        if (self._path is None) or (self._tag_list is None):
            return -1
        
        os.chdir(self._path)
        res = ""
        for tag in self._tag_list:
            try:
                open(tag+".tag", 'a').close()
                print("creating " + tag+".tag")
            except Exception as e:
                res += (e.message + "; ")
                print(res)
        os.chdir(self.BASE_PATH)


class GUI:
    """The GUI/view layer of Create Tag Files"""
    def __init__(self, main_controller):
        """register the controller"""
        if main_controller is None:
            exit(-1)
        self._controller = main_controller

        # main window
        self._frm_root = tk.Frame(width=285, height=210)
        self._frm_root.grid_propagate(0)
        self._frm_root.grid(padx=15, pady=15)

        # input frame
        self._frm_input = tk.Frame(self._frm_root)
        self._frm_input.grid(row=0, padx=5, pady=5)
        # tags row - label
        self._lbl_tags = tk.Label(self._frm_input, text="Tags")
        self._lbl_tags.grid(row=0, column=0, sticky=tk.NW, padx=5)
        # tags row - text input
        self._txt_tags = tk.Text(self._frm_input, width=27, height=10)
        self._txt_tags.grid(row=0, column=1, sticky=tk.E)
        # tags row - text input scroll bar
        self._srb_tags = tk.Scrollbar(self._frm_input,
                                     command=self._txt_tags.yview)
        self._txt_tags.config(yscrollcommand=self._srb_tags)
        self._srb_tags.grid(row=0, column=2, sticky=tk.W+tk.N+tk.S)
        # path row - label
        self._lbl_path = tk.Label(self._frm_input, text="Directory")
        self._lbl_path.grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        # path row - path entry
        self._etr_path = tk.Entry(self._frm_input, width=30)
        self._etr_path.grid(row=1, column=1, columnspan=2, pady=5)

        # button frame
        self._frm_button = tk.Frame(self._frm_root)
        self._frm_button.grid(row=1, padx=3, pady=3)
        # create button
        self._btn_create = tk.Button(self._frm_button, text='Create', width=5)
        self._btn_create.grid(row=0, column=0, sticky=tk.W, padx=30)
        self._btn_create.config(command=self.create_button_click)
        # close button
        self._btn_close = tk.Button(self._frm_button, text='Close', width=5)
        self._btn_close.grid(row=0, column=1, sticky=tk.E, padx=30)
        self._btn_close.config(command=self.close_button_click)

    def close_button_click(self):
        """raise the close event"""
        self._controller.event_raised("close", self)

    def create_button_click(self):
        """raise the create event"""
        self._controller.event_raised("create", self)

    def get_path(self):
        """return the path which users specified"""
        return self._etr_path.get()

    def get_tags(self):
        """return list of tags which users specified"""
        return self._txt_tags.get('1.0', tk.END)

    def quit(self):
        """close the main frame to stop the program"""
        self._frm_root.quit()

    def mainloop(self):
        """start the GUI"""
        self._frm_root.mainloop()


class Controller:
    """The controller which will call the module based on the view's change."""
    def __init__(self, module):
        """register the module"""
        self._process_module = module

    def event_raised(self, event_type, view):
        """handle events, including the close event, the creation event."""
        # the close event handling
        if event_type == "close":
            view.quit()

        # the creation event handling: 
        # get the path and the tags from the view, then set the path and tag 
        # list of the module, then ask the module to create those tag files
        if event_type == "create":
            path = view.get_path()
            tag_list = view.get_tags().split()
            self._process_module.set_path_tags(path, tag_list)
            self._process_module.create_tag_files()

# main program
if __name__ == '__main__':
    # create the process module
    process_module = TagFiles()
    # create the controller, tell the controller which process module to use
    controller = Controller(process_module)
    # create the GUI and, tell the GUI which controller to use
    mainProgram = GUI(controller)
    # start the GUI, waiting user events
    mainProgram.mainloop()
