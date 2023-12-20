from State import State
from OptionsState import OptionsState
import StartState as ss # imported this way to avoid circular import error
import tkinter as tk
import json

class DefaultsState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)
        self.options_state = OptionsState(self.data)
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.options_state.enter(main_frame)

        save_btn = tk.Button(root, text="Save defaults",
                                        command=lambda: DefaultsState.update_defaults(self.options_state.client_id_lb,
                                                                                         self.options_state.date_birth_lb,
                                                                                         self.options_state.rules_fixing_lb,
                                                                                         self.options_state.totals_lb,
                                                                                         self.options_state.to_copy_lb,
                                                                                         self.options_state.priority_lb))
        save_btn.pack(pady=5)

        back_btn = tk.Button(root, text="Back", command=lambda: self.transition(ss.StartState(self.data)))
        back_btn.pack(pady=2)

    def update_defaults(client_id_lb, date_birth_lb, rules_fixing_lb, totals_lb, to_copy_lb, priority_lb):
        client_id_clm = client_id_lb.get(client_id_lb.curselection()[0]) if len(client_id_lb.curselection()) > 0 else None
        date_birth_clm = date_birth_lb.get(date_birth_lb.curselection()[0]) if len(date_birth_lb.curselection()) > 0 else None
        rules_fixing_clms = [rules_fixing_lb.get(idx) for idx in rules_fixing_lb.curselection()]
        totals_clms = [totals_lb.get(idx) for idx in totals_lb.curselection()]
        to_copy_clms = [to_copy_lb.get(idx) for idx in to_copy_lb.curselection()]

        priority_vals = list(priority_lb.get(0, priority_lb.size() - 1))

        data_to_serialise = {"client_id": client_id_clm,
                             "date_birth": date_birth_clm,
                             "rules_fixing": rules_fixing_clms,
                             "totals": totals_clms,
                             "to_copy": to_copy_clms,
                             "priorities": priority_vals}
        
        with open("defaults.json", "w") as f:
            json.dump(data_to_serialise, f)

    def exit(self):
        super().exit()