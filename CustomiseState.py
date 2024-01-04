from State import State
from utils import process_file
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from OptionsState import OptionsState
import StartState as ss

# For further documentation, visit State.py

class CustomiseState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)

        # this state uses Options State as a sub-state to avoid code repetition because
        # it is shared with the Defaults State i.e. the Defaults State uses it as a sub-state too
        options_state = OptionsState(self.data)

        # create a frame (container) for the Options State's widgets.
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # draw options state's widgets onto the frame
        options_state.enter(main_frame)

        process_customise_btn = tk.Button(root, text="Process using the above settings",
                                        command=lambda: self.process_customise(options_state.client_id_lb,
                                                                                         options_state.date_birth_lb,
                                                                                         options_state.rules_fixing_lb,
                                                                                         options_state.totals_lb,
                                                                                         options_state.to_copy_lb,
                                                                                         options_state.priority_lb))
        process_customise_btn.pack(pady=5)

        # back button on click performs a state transition to the Start State
        back_btn = tk.Button(root, text="Back", command=lambda: self.transition(ss.StartState(self.data)))
        back_btn.pack(pady=3)

    def exit(self):
        super().exit()

    # Called when the "Process using the above settings" button is pressed. It extracts the settings from the options state
    # and calls the process_file f-on using them.
    # Args:
    # 1. client_id_lb : tk.ListBox - the listbox containing the selection for the Client ID column
    # 2. date_birth_lb : tk.ListBox - the listbox containing the selection for the Date of Birth column
    # 3. rules_fixing_lb : tk.ListBox - the listbox containing the selections for the columns to apply rule fixing to
    # 4. totals_lb : tk.ListBox - the listbox containing the selections for the columns which can contain "Total"
    # 5. to_copy_lb : tk.ListBox - the listbox containing the selections for the columns to copy from the last row containing "Total"
    # 6. priority_lb : tk.ListBox - the listbox containing the values for rule fixing ordered by priority (first one has most priority)
    def process_customise(self, client_id_lb, date_birth_lb, rules_fixing_lb, totals_lb, to_copy_lb, priority_lb):
        # if there is a setting for which there is no option selected or if the priority list is empty,
        # then show error message and do nothing
        if len(client_id_lb.curselection()) <= 0 or len(date_birth_lb.curselection()) <= 0 or len(rules_fixing_lb.curselection()) <= 0 \
        or len(totals_lb.curselection()) <= 0 or len(to_copy_lb.curselection()) <= 0 or priority_lb.size() <= 0:
            showinfo(title="Error", message="Cannot process the file because some of the selections are empty!")
            return
        
        # extract the settings
        client_id_clm = client_id_lb.get(client_id_lb.curselection()[0])
        date_birth_clm = date_birth_lb.get(date_birth_lb.curselection()[0])
        rules_fixing_clms = [rules_fixing_lb.get(idx) for idx in rules_fixing_lb.curselection()]
        totals_clms = [totals_lb.get(idx) for idx in totals_lb.curselection()]
        to_copy_clms = [to_copy_lb.get(idx) for idx in to_copy_lb.curselection()]

        priority_vals = list(priority_lb.get(0, priority_lb.size() - 1))

        filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                                filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")

        # if the cancel button in the file dialog was pressed, do nothing
        if filename_to_save == "":
            return
        
        # process the file and save it as selected
        final_df = process_file(self.data.filename, client_id_clm, date_birth_clm, totals_clms, rules_fixing_clms, to_copy_clms, priority_vals)
        final_df.to_excel(filename_to_save, index=False)

        showinfo(title="Success!", message="File has been successfully created!")