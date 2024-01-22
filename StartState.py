from State import State
import tkinter as tk
from utils import process_file, read_defaults
from tkinter import filedialog as fd
from CustomiseState import CustomiseState
from DefaultsState import DefaultsState
from tkinter.messagebox import showinfo
import pandas as pd
from tkinter import messagebox

# For further documentation, visit State.py

class StartState(State):
    def __init__(self, data):
        super().__init__(data)

    # Creates all the widgets and sets the layout
    def enter(self, root):
        super().enter(root)
    
        self.msg = tk.Message(root, text="File chosen: " + self.data.filename, width=600-10, bg=self.data.background_clr, font=("Arial", 12))
    
        self.btn_process = tk.Button(root, text="Process using the defaults",
                                      command=self.process_btn_pressed,
                                        state="disabled" if self.data.filename == "None" else "normal")
        self.btn_customise = tk.Button(root, text="Customise",
                                        command=self.customise_btn_pressed,
                                          state="disabled" if self.data.filename == "None" else "normal")
        self.btn_edit_defaults = tk.Button(root, text="Edit the defaults",
                                            command=self.edit_defaults_btn_pressed,
                                              state="disabled" if self.data.filename == "None" else "normal")

        self.btn_open = tk.Button(root, text="Open file", command=lambda: self.open_file_btn_pressed(self.msg,
                                                                                                      self.btn_process, self.btn_customise, self.btn_edit_defaults))

        self.msg.pack(side=tk.TOP, pady=10, fill=tk.X)
        self.btn_open.pack(pady=1.5)
        self.btn_process.pack(pady=1.5)
        self.btn_customise.pack(pady=1.5)
        self.btn_edit_defaults.pack(pady=1.5)

    def exit(self):
        super().exit()

    # Called when the "Open File" button is pressed. It opens up the file and enables the other buttons
    # Args:
    # 1. msg : tk.Message - the message widget to update with the new file name
    # 2. btn_process : tk.Button - the "Process using the defaults" button widget
    # 3. btn_customise : tk.Button - the "Customise" button widget
    # 4. btn_edit_defaults : tk.Button - the "Edit the defaults" button widget
    def open_file_btn_pressed(self, msg, btn_process, btn_customise, btn_edit_defaults):
        # open the file selection dialog
        filename_to_open = fd.askopenfilename(title="Choose the file with legal data to be cleaned up",
                                    filetypes=(("Excel file (.xlsx) or CSV (.csv)", ".xlsx .csv"),
                                               ("Excel file (.xlsx)", ".xlsx"),
                                               ("Comma Separated Values file (.csv)", ".csv")))
        
        if filename_to_open == "":
            return
        
        self.data.filename = filename_to_open
        
        # change the text in the top to reflect the new opened file
        self.msg.configure(text="File chosen: " + self.data.filename)

        # enable the other buttons below it
        self.btn_process.configure(state="normal")
        self.btn_customise.configure(state="normal")
        self.btn_edit_defaults.configure(state="normal")


    # Called when the "Process using defaults" button is pressed. It reads the defaults from the defaults.json
    # file and pops out a file dialog so that you choose where to save. Then it processes the file and saves
    # it as chosen.
    def process_btn_pressed(self):
        # read the defaults
        default_client_id, default_date_birth, default_rules_fixing, default_totals, \
        default_to_copy, default_priorities = read_defaults()

        # if any of the defaults are missing, throw an error message
        if default_client_id is None or default_date_birth is None or len(default_rules_fixing) <= 0 \
        or len(default_totals) <= 0 or len(default_to_copy) <= 0 or len(default_priorities) <= 0:
            messagebox.showerror(title="Error", message="Error, invalid defaults! Cannot process file.")
            return

        # saving file dialog
        filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                                filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")
        
        # if cancel was pressed, do nothing
        if filename_to_save == "":
            return
        
        # process the file using all of the gathered parameters
        final_df = process_file(self.data.filename, id_column=default_client_id, date_of_birth_column=default_date_birth,
                                columns_to_check_for_total=default_totals, columns_for_rule_fixing=default_rules_fixing,
                                columns_to_copy_from_last_total=default_to_copy, priority_vals=default_priorities)

        # there was a column selected that does not exist in this file. Most likely the defaults
        # contain a column that is not present in this file. Do nothing in this case and just display
        # the error message
        if final_df is None:
            messagebox.showerror("Error! Column does not exist in file!",
                     "One or more columns selected for processing do not exist in this file. Please go to the Customise screen where they will be highlighted in red.")
            return

        # save the file
        final_df.to_excel(filename_to_save, index=False)

        showinfo(title="Success!", message="File has been successfully created!")

    # Called when the "Customise" button gets pressed. Performs a state transition to the Customise state
    def customise_btn_pressed(self):
        self.transition(CustomiseState(self.data))

    # Called when the "Edit the defaults" button gets pressed. Performs a state transition to the Defaults
    # state
    def edit_defaults_btn_pressed(self):
        self.transition(DefaultsState(self.data))