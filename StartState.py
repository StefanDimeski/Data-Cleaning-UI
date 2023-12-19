from State import State
import tkinter as tk
from utils import process_file
from tkinter import filedialog as fd

class StartState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)
    
        self.msg = tk.Message(root, text="File chosen: " + self.data.filename, width=600-10, bg=self.data.background_clr, font=("Arial", 12))
    
        self.btn_process = tk.Button(root, text="Process using the defaults", command=self.process_btn_pressed, state="disabled")
        self.btn_customise = tk.Button(root, text="Customise", command=self.customise_btn_pressed, state="disabled")
        self.btn_edit_defaults = tk.Button(root, text="Edit the defaults", command=self.edit_defaults_btn_pressed, state="disabled")

        self.btn_open = tk.Button(root, text="Open file", command=lambda: self.open_file_btn_pressed(self.msg,
                                                                                                      self.btn_process, self.btn_customise, self.btn_edit_defaults))

        self.msg.pack(side=tk.TOP, pady=10, fill=tk.X)
        self.btn_open.pack(pady=1.5)
        self.btn_process.pack(pady=1.5)
        self.btn_customise.pack(pady=1.5)
        self.btn_edit_defaults.pack(pady=1.5)

    def open_file_btn_pressed(self, msg, btn_process, btn_customise, btn_edit_defaults):
        self.data.filename = fd.askopenfilename(title="Choose the file with legal data to be cleaned up",
                                    filetypes=(("Excel files (.xlsx)", "*.xlsx"),))
        
        self.msg.configure(text="File chosen: " + self.data.filename)

        self.btn_process.configure(state="normal")
        self.btn_customise.configure(state="normal")
        self.btn_edit_defaults.configure(state="normal")

    def process_btn_pressed(self):
        filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                                filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")
        
        clms_for_rule_fixing = ["Financial Disadvantage Indicator", "Family Violence Indicator", "Disability", "Homelessness Status"]
        clms_to_check_for_total = ["Country Of Birth"] + clms_for_rule_fixing
        clms_to_copy_from_last_total = ["Court/Tribunal", "Information", "Legal Advice", "Legal Task", "Other Representation", "Referral", "Triage", "Grand Total"]
        
        final_df = process_file(self.data.filename, id_column="Client ID", date_of_birth_column="Date Of Birth",
                                columns_to_check_for_total=clms_to_check_for_total, columns_for_rule_fixing=clms_for_rule_fixing,
                                columns_to_copy_from_last_total=clms_to_copy_from_last_total)

        final_df.to_excel(filename_to_save, index=False)

        # Close the app, ASK ANAS IF IT SHOULD CLOSE AUTOMATICALLY OR NOT
        self.root.destroy()

    def customise_btn_pressed():
        #self.transition()
        pass

    def edit_defaults_btn_pressed(self):
        for child in root.winfo_children():
            child.destroy()

    pass