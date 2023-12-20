from State import State
import tkinter as tk
from utils import process_file, read_defaults
from tkinter import filedialog as fd
from CustomiseState import CustomiseState
from DefaultsState import DefaultsState
from tkinter.messagebox import showinfo

class StartState(State):
    def __init__(self, data):
        super().__init__(data)

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

    def open_file_btn_pressed(self, msg, btn_process, btn_customise, btn_edit_defaults):
        filename_to_open = fd.askopenfilename(title="Choose the file with legal data to be cleaned up",
                                    filetypes=(("Excel files (.xlsx)", "*.xlsx"),))
        
        if filename_to_open == "":
            return
        
        self.data.filename = filename_to_open
        
        self.msg.configure(text="File chosen: " + self.data.filename)

        self.btn_process.configure(state="normal")
        self.btn_customise.configure(state="normal")
        self.btn_edit_defaults.configure(state="normal")

    def process_btn_pressed(self):
        default_client_id, default_date_birth, default_rules_fixing, default_totals, \
        default_to_copy, default_priorities = read_defaults()

        if default_client_id is None or default_date_birth is None or len(default_rules_fixing) <= 0 \
        or len(default_totals) <= 0 or len(default_to_copy) <= 0 or len(default_priorities) <= 0:
            showinfo(title="Error", message="Error, invalid defaults! Cannot process file.")
            return

        filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                                filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")
        
        if filename_to_save == "":
            return
        
        final_df = process_file(self.data.filename, id_column=default_client_id, date_of_birth_column=default_date_birth,
                                columns_to_check_for_total=default_totals, columns_for_rule_fixing=default_rules_fixing,
                                columns_to_copy_from_last_total=default_to_copy, priority_vals=default_priorities)

        final_df.to_excel(filename_to_save, index=False)

        # Close the app, ASK ANAS IF IT SHOULD CLOSE AUTOMATICALLY OR NOT
        #self.root.destroy()

    def customise_btn_pressed(self):
        self.transition(CustomiseState(self.data))

    def edit_defaults_btn_pressed(self):
        self.transition(DefaultsState(self.data))