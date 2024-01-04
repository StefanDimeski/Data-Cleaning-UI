from State import State
from OptionsState import OptionsState
import StartState as ss # imported this way to avoid circular import error
import tkinter as tk
import json

# For further documentation, visit State.py

class DefaultsState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)

        # this state uses Options State as a sub-state to avoid code repetition because
        # it is shared with the Customise State i.e. the Customise State uses it as a sub-state too
        self.options_state = OptionsState(self.data)

        # create a frame (container) for the Options State widgets.
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # draw options state's widgets onto the frame
        self.options_state.enter(main_frame)

        save_btn = tk.Button(root, text="Save defaults",
                                        command=lambda: DefaultsState.update_defaults(self.options_state.client_id_lb,
                                                                                         self.options_state.date_birth_lb,
                                                                                         self.options_state.rules_fixing_lb,
                                                                                         self.options_state.totals_lb,
                                                                                         self.options_state.to_copy_lb,
                                                                                         self.options_state.priority_lb))
        save_btn.pack(pady=5)

        # back button on click performs a state transition to the Start State
        back_btn = tk.Button(root, text="Back", command=lambda: self.transition(ss.StartState(self.data)))
        back_btn.pack(pady=2)

    # Called when the "Save defaults" button is pressed. It first reads out the selections from the widgets
    # and then saves them to the defaults.json file in JSON format.
    # Args:
    # 1. client_id_lb : tk.ListBox - the listbox containing the selection for the Client ID column
    # 2. date_birth_lb : tk.ListBox - the listbox containing the selection for the Date of Birth column
    # 3. rules_fixing_lb : tk.ListBox - the listbox containing the selections for the columns to apply rule fixing to
    # 4. totals_lb : tk.ListBox - the listbox containing the selections for the columns which can contain "Total"
    # 5. to_copy_lb : tk.ListBox - the listbox containing the selections for the columns to copy from the last row containing "Total"
    # 6. priority_lb : tk.ListBox - the listbox containing the values for rule fixing ordered by priority (first one has most priority)
    def update_defaults(client_id_lb, date_birth_lb, rules_fixing_lb, totals_lb, to_copy_lb, priority_lb):
        # read out the selections from the widgets
        client_id_clm = client_id_lb.get(client_id_lb.curselection()[0]) if len(client_id_lb.curselection()) > 0 else None
        date_birth_clm = date_birth_lb.get(date_birth_lb.curselection()[0]) if len(date_birth_lb.curselection()) > 0 else None
        rules_fixing_clms = [rules_fixing_lb.get(idx) for idx in rules_fixing_lb.curselection()]
        totals_clms = [totals_lb.get(idx) for idx in totals_lb.curselection()]
        to_copy_clms = [to_copy_lb.get(idx) for idx in to_copy_lb.curselection()]

        priority_vals = list(priority_lb.get(0, priority_lb.size() - 1))

        # create a dictionary of the data to save
        data_to_serialise = {"client_id": client_id_clm,
                             "date_birth": date_birth_clm,
                             "rules_fixing": rules_fixing_clms,
                             "totals": totals_clms,
                             "to_copy": to_copy_clms,
                             "priorities": priority_vals}
        
        # write the dictionary to the file
        with open("defaults.json", "w") as f:
            json.dump(data_to_serialise, f, indent=4)

    def exit(self):
        super().exit()