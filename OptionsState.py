from State import State
import pandas as pd
import tkinter as tk
from tkinter import simpledialog as sd
from utils import read_defaults
from tkinter.messagebox import showinfo

# For further documentation, visit State.py

class OptionsState(State):
    def __init__(self, data):
        super().__init__(data)

    def enter(self, root):
        super().enter(root)

        # get the selected file's extension
        file_extension = self.data.filename.split(".")[-1]

        if file_extension == 'csv':
            df = pd.read_csv(self.data.filename, encoding='cp1252')
        elif file_extension == 'xlsx':
            df = pd.read_excel(self.data.filename)
        else:
            print("Shouldn't have gotten here")

        # if the first row is not the actual column names, read them from the second row.
        # This happens due to the system used in WCC which generates an extra unneeded row at the top
        if len(list(filter(lambda x: x is None or x == "" or "Unnamed:" in x, df.columns))) > 0:
            # read the real column names from the second row of the actual file (i.e. first row here
            # since the read columns do not count as a row)
            column_names = list(df.iloc[0])

            # discard the row with the real column names
            df = df.iloc[1:]

            # replace the wrong column names with the correct ones
            df.columns = column_names

        
        # get the defaults
        default_client_id, default_date_birth, default_rules_fixing, default_totals, \
        default_to_copy, default_priorities = read_defaults()

        # cofigure three columns with equal weight meaning they will split the
        # available space evenly
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # configure two rows with equal weight meaning they will split the 
        # available space evenly
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        # flag which is set to true when a column is in the defaults but does not exist in
        # the currently opened file. I use this to determine whether to show a message at
        # the end of this function
        default_column_not_present_detected = False

        ###### Create the Client ID section (documentation provided only for this section, the rest of them
        #                                   are identical)
  
        # frame that will contain the whole section i.e. root frame for the section
        client_id_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
        client_id_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        client_id_txt = tk.Message(client_id_frame, text="Select the column which contains the Client ID:", width=600-10)
        client_id_txt.pack()

        # frame for the listbox and scrollbar
        client_id_lb_frame = tk.Frame(client_id_frame)
        client_id_lb_frame.pack(fill=tk.BOTH, padx=4, expand=True)

        self.client_id_lb = tk.Listbox(client_id_lb_frame, exportselection=False)
        self.client_id_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        client_id_sb = tk.Scrollbar(client_id_lb_frame)
        client_id_sb.pack(side=tk.RIGHT, fill=tk.Y)

        # add all the columns of the file to the listbox
        for column in df.columns:
            self.client_id_lb.insert(tk.END, str(column))

            # select the default client id column
            if column == default_client_id:
                self.client_id_lb.select_set(tk.END)
                self.client_id_lb.event_generate("<<ListboxSelect>>")
                self.client_id_lb.see(tk.END)

        # Check if the default column for this section exists in the currently opened file.
        # If not, add it at the top of the list, highlighted in red colour
        if default_client_id not in df.columns:
            self.client_id_lb.insert(0, str(default_client_id))
            self.client_id_lb.itemconfig(0, background='red', foreground='black', selectbackground='#0078d7', selectforeground='red')
            self.client_id_lb.see(0)

            default_column_not_present_detected = True

        client_id_sb.config(command=self.client_id_lb.yview)
        self.client_id_lb.config(yscrollcommand=client_id_sb.set)

        ###### Create the date of birth section

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


        if default_date_birth not in df.columns:
            self.date_birth_lb.insert(0, str(default_date_birth))
            self.date_birth_lb.itemconfig(0, background='red', foreground='black', selectbackground='#0078d7', selectforeground='red')
            self.date_birth_lb.see(0)

            default_column_not_present_detected = True

        date_birth_sb.config(command=self.date_birth_lb.yview)
        self.date_birth_lb.config(yscrollcommand=date_birth_sb.set)

        ###### Create the rules fixing section

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

        # Check if the default columns for this section exist in the currently opened file.
        # If not, add the ones that are not present at the top of the list, highlighted in red colour
        for column in default_rules_fixing:
            if column not in df.columns:
                self.rules_fixing_lb.insert(0, str(column))
                self.rules_fixing_lb.itemconfig(0, background='red', foreground='black', selectbackground='#0078d7', selectforeground='red')
                self.rules_fixing_lb.see(0)

                default_column_not_present_detected = True

        rules_fixing_sb.config(command=self.rules_fixing_lb.yview)
        self.rules_fixing_lb.config(yscrollcommand=rules_fixing_sb.set)

        # rules_fixing_lb.activate(3) check if u can get rid of the underline when deselecting with this

        ###### Create the totals section

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

        for column in default_totals:
            if column not in df.columns:
                self.totals_lb.insert(0, str(column))
                self.totals_lb.itemconfig(0, background='red', foreground='black', selectbackground='#0078d7', selectforeground='red')
                self.totals_lb.see(0)

                default_column_not_present_detected = True

        totals_sb.config(command=self.totals_lb.yview)
        self.totals_lb.config(yscrollcommand=totals_sb.set)

        ###### Create the to copy section

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

        for column in default_to_copy:
            if column not in df.columns:
                self.to_copy_lb.insert(0, str(column))
                self.to_copy_lb.itemconfig(0, background='red', foreground='black', selectbackground='#0078d7', selectforeground='red')
                self.to_copy_lb.see(0)

                default_column_not_present_detected = True

        to_copy_sb.config(command=self.to_copy_lb.yview)
        self.to_copy_lb.config(yscrollcommand=to_copy_sb.set)

        ###### Create the priority values section

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

        # If there was at least one default column that doesn't exist in the currently opened file
        # display a info message
        if default_column_not_present_detected:
            showinfo("Some default columns not present in the opened file!",
                     "One or more of the default columns are not present in this file. They are highlighted in red colour in their respective sections. They have been automatically deselected for you. You may wish to edit the defaults if those columns are no longer in use.")

    # Called when the "Add new" button is pressed for the priority values.
    # Pops up a dialog box asking for a string and then adds that string to listbox
    # after the currently selected item
    # Args:
    # 1. listbox : tk.Listbox - listbox to which to add the new value
    def priority_add(listbox):
        # ask for the new value
        val_to_add = sd.askstring(title="Adding a new value", prompt="Enter the new value to add:")

        # if cancel was pressed on the dialog, do nothing
        if val_to_add is None:
            return
        
        # add it to the beginning if the listbox is empty otherwise add it after the currently selected item
        idx_to_add_to = 0 if listbox.size() <= 0 else listbox.curselection()[0]
        listbox.insert(idx_to_add_to + 1, val_to_add)

        # select the newly added value
        listbox.selection_clear(0, tk.END)
        listbox.select_set(idx_to_add_to + 1)
        listbox.event_generate("<<ListboxSelect>>")

    # Called when the "Remove selected" button is pressed for the priority vals. Removes the selected value/item
    # from listbox
    # Args:
    # 1. listbox : tk.Listbox - listbox from which to remove the selected value
    def priority_remove(listbox):
        # get the currently selected value
        idx_selected = listbox.curselection()[0]

        # delete it
        listbox.delete(idx_selected)

        # if the listbox is now empty, our job is done
        if listbox.size() <= 0:
            return

        # at this point the listbox is not empty, so select/highlight the newly added value
        if idx_selected - 1 < 0:
            listbox.select_set(0) #This only sets focus on the first item.
        else:
            listbox.select_set(idx_selected - 1)

        listbox.event_generate("<<ListboxSelect>>")

    # Called when the "Move selected up" button is pressed for the priority vals.
    # Moves the selected value up by one place in the list.
    # Args:
    # 1. listbox : tk.Listbox - listbox in which to move the selected value
    def priority_up(listbox):
        # get the currently selected item
        curr_sel = listbox.curselection()

        # if the listbox is empty or the first item is selected, then do nothing
        if listbox.size() <= 0 or curr_sel[0] == 0:
            print("empty list or first item selected")
            return
        
        # temporarily save the value we are going to move
        txt = listbox.get(curr_sel[0])

        # delete the value from its previous position
        listbox.delete(curr_sel[0])
        # add the value on its new position
        listbox.insert(curr_sel[0] - 1, txt)

        # highlight/select the value in its new position
        listbox.select_set(curr_sel[0] - 1)
        listbox.event_generate("<<ListboxSelect>>")

    # Called when the "Move selected down" button is pressed for the priority vals.
    # Moves the selected value down by one place in the list.
    # Args:
    # 1. listbox : tk.Listbox - listbox in which to move the selected value
    def priority_down(listbox):
        # same logic as in the priority_up function, just moving one position down instead of up
        curr_sel = listbox.curselection()

        if listbox.size() <= 0 or curr_sel[0] == listbox.size() - 1:
            print("empty list or last item selected")
            return
        
        txt = listbox.get(curr_sel[0])

        listbox.delete(curr_sel[0])
        listbox.insert(curr_sel[0] + 1, txt)

        listbox.select_set(curr_sel[0] + 1)
        listbox.event_generate("<<ListboxSelect>>")

    # Called when the "Edit selected" button is pressed for the priority vals.
    # Edits the currently selected value.
    # Args:
    # 1. listbox : tk.Listbox - listbox in which to edit the currently selected value
    def priority_edit(listbox):
        # if the listbox is empty, do nothing
        if listbox.size() <= 0:
            return
        
        # get the currently selected item
        curr_sel = listbox.curselection()[0]

        # pop up a dialog asking for the new value
        new_txt = sd.askstring(title="Changing value", prompt="Enter the new value: ", initialvalue=listbox.get(curr_sel))

        # if they didnt press cancel on the dialog, change the value to the new one
        if new_txt is not None:
            # delete the old value
            listbox.delete(curr_sel)

            # replace it with the new value i.e. insert the new value in the same place as the old one
            listbox.insert(curr_sel, new_txt)

            # select/highlight the new value
            listbox.select_set(curr_sel)
            listbox.event_generate("<<ListboxSelect>>")
    
    def exit(self):
        super().exit()