from State import State
import pandas as pd
import tkinter as tk
from tkinter import simpledialog as sd
from utils import read_defaults

class OptionsState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)

        file_extension = self.data.filename.split(".")[-1]

        if file_extension == 'csv':
            df = pd.read_csv(self.data.filename)
        elif file_extension == 'xlsx':
            df = pd.read_excel(self.data.filename)
        else:
            print("Shouldn't have gotten here")

        

        default_client_id, default_date_birth, default_rules_fixing, default_totals, \
        default_to_copy, default_priorities = read_defaults()

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
  
        client_id_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        client_id_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        client_id_txt = tk.Message(client_id_frame, text="Select the column which contains the Client ID:", width=600-10)
        client_id_txt.pack()

        client_id_lb_frame = tk.Frame(client_id_frame)
        client_id_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.client_id_lb = tk.Listbox(client_id_lb_frame, exportselection=False)
        self.client_id_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        client_id_sb = tk.Scrollbar(client_id_lb_frame)
        client_id_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for column in df.columns:
            self.client_id_lb.insert(tk.END, str(column))
            if column == default_client_id:
                self.client_id_lb.select_set(tk.END)
                self.client_id_lb.event_generate("<<ListboxSelect>>")
                self.client_id_lb.see(tk.END)

        client_id_sb.config(command=self.client_id_lb.yview)
        self.client_id_lb.config(yscrollcommand=client_id_sb.set)

        ######

        date_birth_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        date_birth_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        date_birth_txt = tk.Message(date_birth_frame, text="Select the column which contains the Date Of Birth:", width=600-10)
        date_birth_txt.pack()

        date_birth_lb_frame = tk.Frame(date_birth_frame)
        date_birth_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.date_birth_lb = tk.Listbox(date_birth_lb_frame, exportselection=False)
        self.date_birth_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        date_birth_sb = tk.Scrollbar(date_birth_lb_frame)
        date_birth_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for column in df.columns:
            self.date_birth_lb.insert(tk.END, str(column))

            if column == default_date_birth:
                self.date_birth_lb.select_set(tk.END)
                self.date_birth_lb.event_generate("<<ListboxSelect>>")
                self.date_birth_lb.see(tk.END)

        date_birth_sb.config(command=self.date_birth_lb.yview)
        self.date_birth_lb.config(yscrollcommand=date_birth_sb.set)

        #####

        rules_fixing_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        rules_fixing_frame.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

        rules_fixing_txt = tk.Message(rules_fixing_frame, text="Select the columns to which rule fixing should be applied:", width=600-10)
        rules_fixing_txt.pack()

        rules_fixing_lb_frame = tk.Frame(rules_fixing_frame)
        rules_fixing_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.rules_fixing_lb = tk.Listbox(rules_fixing_lb_frame, exportselection=False, selectmode="multiple")
        self.rules_fixing_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        rules_fixing_sb = tk.Scrollbar(rules_fixing_lb_frame)
        rules_fixing_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for column in df.columns:
            self.rules_fixing_lb.insert(tk.END, str(column))

            if column in default_rules_fixing:
                self.rules_fixing_lb.select_set(tk.END)
                self.rules_fixing_lb.event_generate("<<ListboxSelect>>")
                self.rules_fixing_lb.see(tk.END)

        rules_fixing_sb.config(command=self.rules_fixing_lb.yview)
        self.rules_fixing_lb.config(yscrollcommand=rules_fixing_sb.set)

        # rules_fixing_lb.activate(3) check if u can get rid of the underline when deselecting with this

        #####

        totals_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        totals_frame.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

        totals_txt = tk.Message(totals_frame, text="Select the columns that should be checked for 'Total':", width=600-10)
        totals_txt.pack()

        totals_lb_frame = tk.Frame(totals_frame)
        totals_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.totals_lb = tk.Listbox(totals_lb_frame, exportselection=False, selectmode="multiple")
        self.totals_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        totals_sb = tk.Scrollbar(totals_lb_frame)
        totals_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for column in df.columns:
            self.totals_lb.insert(tk.END, str(column))

            if column in default_totals:
                self.totals_lb.select_set(tk.END)
                self.totals_lb.event_generate("<<ListboxSelect>>")
                self.totals_lb.see(tk.END)

        totals_sb.config(command=self.totals_lb.yview)
        self.totals_lb.config(yscrollcommand=totals_sb.set)

        #####

        to_copy_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        to_copy_frame.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")

        to_copy_txt = tk.Message(to_copy_frame, text="Select the columns that are copied from the last totals row:", width=600-10)
        to_copy_txt.pack()

        to_copy_lb_frame = tk.Frame(to_copy_frame)
        to_copy_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.to_copy_lb = tk.Listbox(to_copy_lb_frame, exportselection=False, selectmode="multiple")
        self.to_copy_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        to_copy_sb = tk.Scrollbar(to_copy_lb_frame)
        to_copy_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for column in df.columns:
            self.to_copy_lb.insert(tk.END, str(column))

            if column in default_to_copy:
                self.to_copy_lb.select_set(tk.END)
                self.to_copy_lb.event_generate("<<ListboxSelect>>")
                self.to_copy_lb.see(tk.END)

        to_copy_sb.config(command=self.to_copy_lb.yview)
        self.to_copy_lb.config(yscrollcommand=to_copy_sb.set)

        #####

        priority_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        priority_frame.grid(row=1, column=2, padx=3, pady=3, sticky="nsew")

        priority_txt = tk.Message(priority_frame, text="Arrange the priority of the values for rule-fixing:", width=600-10)
        priority_txt.pack()

        priority_lb_frame = tk.Frame(priority_frame)
        priority_lb_frame.pack(side=tk.LEFT, padx=4, fill=tk.BOTH, expand=True)

        self.priority_lb = tk.Listbox(priority_lb_frame, exportselection=False)
        self.priority_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        priority_sb = tk.Scrollbar(priority_lb_frame)
        priority_sb.pack(side=tk.RIGHT, fill=tk.Y)

        for val in default_priorities:
            self.priority_lb.insert(tk.END, str(val))

        priority_sb.config(command=self.priority_lb.yview)
        self.priority_lb.config(yscrollcommand=priority_sb.set)

        self.priority_lb.select_set(0) # Set focus on the first item.
        self.priority_lb.event_generate("<<ListboxSelect>>")

        priority_btns_frame = tk.Frame(priority_frame)
        priority_btns_frame.pack(side=tk.RIGHT, padx=4)

        priority_add_btn = tk.Button(priority_btns_frame, text="Add new", command=lambda: OptionsState.priority_add(self.priority_lb))
        priority_add_btn.pack(pady=1.5)

        priority_remove_btn = tk.Button(priority_btns_frame, text="Remove selected", command=lambda: OptionsState.priority_remove(self.priority_lb))
        priority_remove_btn.pack(pady=1.5)

        priority_up_btn = tk.Button(priority_btns_frame, text="Move selected up", command=lambda: OptionsState.priority_up(self.priority_lb))
        priority_up_btn.pack(pady=1.5)

        priority_down_btn = tk.Button(priority_btns_frame, text="Move selected down", command=lambda: OptionsState.priority_down(self.priority_lb))
        priority_down_btn.pack(pady=1.5)

        priority_edit_btn = tk.Button(priority_btns_frame, text="Edit selected", command=lambda: OptionsState.priority_edit(self.priority_lb))
        priority_edit_btn.pack(pady=1.5)

    
    def priority_add(listbox):
        val_to_add = sd.askstring(title="Adding a new value", prompt="Enter the new value to add:")

        if val_to_add is None:
            return
        
        idx_to_add_to = 0 if listbox.size() <= 0 else listbox.curselection()[0]
        listbox.insert(idx_to_add_to + 1, val_to_add)

        listbox.selection_clear(0, tk.END)

        listbox.select_set(idx_to_add_to + 1)
        listbox.event_generate("<<ListboxSelect>>")

    def priority_remove(listbox):
        idx_selected = listbox.curselection()[0]

        listbox.delete(idx_selected)

        if listbox.size() <= 0:
            return

        if idx_selected - 1 < 0:
            listbox.select_set(0) #This only sets focus on the first item.
        else:
            listbox.select_set(idx_selected - 1)

        listbox.event_generate("<<ListboxSelect>>")

    def priority_up(listbox):
        curr_sel = listbox.curselection()

        if listbox.size() <= 0 or curr_sel[0] == 0:
            print("empty list or first item selected")
            return
        
        txt = listbox.get(curr_sel[0])

        listbox.delete(curr_sel[0])
        listbox.insert(curr_sel[0] - 1, txt)

        listbox.select_set(curr_sel[0] - 1)
        listbox.event_generate("<<ListboxSelect>>")


    def priority_down(listbox):
        curr_sel = listbox.curselection()

        if listbox.size() <= 0 or curr_sel[0] == listbox.size() - 1:
            print("empty list or last item selected")
            return
        
        txt = listbox.get(curr_sel[0])

        listbox.delete(curr_sel[0])
        listbox.insert(curr_sel[0] + 1, txt)

        listbox.select_set(curr_sel[0] + 1)
        listbox.event_generate("<<ListboxSelect>>")

    def priority_edit(listbox):
        if listbox.size() <= 0:
            return
        
        curr_sel = listbox.curselection()[0]

        new_txt = sd.askstring(title="Changing value", prompt="Enter the new value: ", initialvalue=listbox.get(curr_sel))

        if new_txt is not None:
            listbox.delete(curr_sel)
            listbox.insert(curr_sel, new_txt)

            listbox.select_set(curr_sel)
            listbox.event_generate("<<ListboxSelect>>")
    
    def exit(self):
        super().exit()