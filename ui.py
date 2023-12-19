import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter.messagebox import showinfo
import pandas as pd

# FIX THAT PROCESSING A PROCESSED FILE DOESNT WORK BECAUSE OF THE DATE TIME THING WITH DATE OF BIRTH

def open_file_btn_pressed(msg, btn_process, btn_customise, btn_edit_defaults):
    global filename
    
    filename = fd.askopenfilename(title="Choose the file with legal data to be cleaned up",
                                filetypes=(("Excel files (.xlsx)", "*.xlsx"),))
    
    msg.configure(text="File chosen: " + filename)

    btn_process.configure(state="normal")
    btn_customise.configure(state="normal")
    btn_edit_defaults.configure(state="normal")



def process_file(filepath, id_column, date_of_birth_column, columns_to_check_for_total, columns_for_rule_fixing, columns_to_copy_from_last_total):
    df = pd.read_excel(filepath)

    df[date_of_birth_column] = df[date_of_birth_column].dt.strftime("%d/%m/%Y")
    df[id_column].ffill(inplace=True)

    # convert all columns which are not ints to string (SHOULD CHECK FOR FLOAT AS WELL)
    df = df.astype({column : "string" for column, dtype in zip(df.columns, df.dtypes) if not 'int' in str(dtype)})

    df[columns_to_check_for_total] = df[columns_to_check_for_total].fillna('')
    
    counts = df.groupby(id_column).size() # get the frequencies of each client ID

    # we are only concerned about the duplicates i.e. users that have multiple entries
    duplicates = counts[counts > 1]

    for curr_client_id in duplicates.index.to_list():
        curr_client_df = df[df[id_column] == curr_client_id]

        totals_rows = pd.DataFrame()
        for column in columns_to_check_for_total:
            curr_totals_rows = curr_client_df[curr_client_df[column].str.contains("Total")]

            # ARE THEY SORTED AS THEY SHOULD BE HERE OR WE'RE NOT GETTING THE CORRECT LAST TOTALS ROW??

            # This is to fix: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
            # In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
            # To retain the old behavior, exclude the relevant entries before the concat operation.
            if curr_totals_rows.empty:
                continue
            elif totals_rows.empty:
                totals_rows = curr_totals_rows
            else:
                totals_rows = pd.concat([totals_rows, curr_totals_rows])

        non_total_rows = curr_client_df.loc[list(set(curr_client_df.index) - set(totals_rows.index))]

        for column in columns_for_rule_fixing:
            values = non_total_rows[column].to_list()

            final_val = None

            for comp in ['Yes', 'At Risk', 'No', "Not applicable", "Unknown"]:
                containing_values = list(filter(lambda val: comp in val, values))
                if len(containing_values) > 0:
                    final_val = containing_values[0]
                    break

            if final_val is not None:
                df.loc[curr_client_df.index[0], column] = final_val
            else:
                df.loc[curr_client_df.index[0], column] = ''

        index_of_last_totals_row = max(list(totals_rows.index))

        df.loc[curr_client_df.index[0], columns_to_copy_from_last_total] = df.loc[index_of_last_totals_row, columns_to_copy_from_last_total]

        df.drop(curr_client_df.index[1:], inplace=True)

    return df


def process_btn_pressed():
    filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                             filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")
    
    clms_for_rule_fixing = ["Financial Disadvantage Indicator", "Family Violence Indicator", "Disability", "Homelessness Status"]
    clms_to_check_for_total = ["Country Of Birth"] + clms_for_rule_fixing
    clms_to_copy_from_last_total = ["Court/Tribunal", "Information", "Legal Advice", "Legal Task", "Other Representation", "Referral", "Triage", "Grand Total"]
    
    final_df = process_file(filename, id_column="Client ID", date_of_birth_column="Date Of Birth",
                            columns_to_check_for_total=clms_to_check_for_total, columns_for_rule_fixing=clms_for_rule_fixing,
                            columns_to_copy_from_last_total=clms_to_copy_from_last_total)

    final_df.to_excel(filename_to_save, index=False)

    # Close the app, ASK ANAS IF IT SHOULD CLOSE AUTOMATICALLY OR NOT
    root.destroy()


def priority_add(listbox):
    val_to_add = sd.askstring(title="Adding a new value", prompt="Enter the new value to add:")

    if val_to_add is None:
        return
    
    idx_to_add_to = 0 if listbox.size() <= 0 else listbox.curselection()[0]
    listbox.insert(idx_to_add_to, val_to_add)

    listbox.selection_clear(0, tk.END)

    listbox.select_set(idx_to_add_to)
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

def process_customise(client_id_lb, date_birth_lb, rules_fixing_lb, totals_lb, to_copy_lb, priority_lb):
    global filename

    if len(client_id_lb.curselection()) <= 0 or len(date_birth_lb.curselection()) <= 0 or len(rules_fixing_lb.curselection()) <= 0 \
    or len(totals_lb.curselection()) <= 0 or len(to_copy_lb.curselection()) <= 0 or priority_lb.size() <= 0:
        showinfo(title="Error", message="Cannot process the file because some of the selections are empty!")
        return
    
    client_id_clm = client_id_lb.get(client_id_lb.curselection()[0])
    date_birth_clm = date_birth_lb.get(date_birth_lb.curselection()[0])
    rules_fixing_clms = [rules_fixing_lb.get(idx) for idx in rules_fixing_lb.curselection()]
    totals_clms = [totals_lb.get(idx) for idx in totals_lb.curselection()]
    to_copy_clms = [to_copy_lb.get(idx) for idx in to_copy_lb.curselection()]

    priority_vals = list(priority_lb.get(0, priority_lb.size() - 1))

    filename_to_save = fd.asksaveasfilename(title="Save as", defaultextension=".xlsx",
                                             filetypes=(("Excel file", ".xlsx"),), confirmoverwrite=True, initialfile="processed_file")

    final_df = process_file(filename, client_id_clm, date_birth_clm, totals_clms, rules_fixing_clms, to_copy_clms)
    final_df.to_excel(filename_to_save, index=False)

def customise_btn_pressed():
    for child in root.winfo_children():
        child.destroy()

    df = pd.read_excel(filename)

    client_id_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    client_id_frame.grid(row=0, column=0)

    client_id_txt = tk.Message(client_id_frame, text="Select the column which contains the Client ID:", width=600-10)
    client_id_txt.pack()

    client_id_lb_frame = tk.Frame(client_id_frame)
    client_id_lb_frame.pack()

    client_id_lb = tk.Listbox(client_id_lb_frame, exportselection=False)
    client_id_lb.pack(side=tk.LEFT, fill=tk.Y)

    client_id_sb = tk.Scrollbar(client_id_lb_frame)
    client_id_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in df.columns:
        client_id_lb.insert(tk.END, str(column))

    client_id_sb.config(command=client_id_lb.yview)
    client_id_lb.config(yscrollcommand=client_id_sb.set)

    ######

    date_birth_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    date_birth_frame.grid(row=0, column=1)

    date_birth_txt = tk.Message(date_birth_frame, text="Select the column which contains the Date Of Birth:", width=600-10)
    date_birth_txt.pack()

    date_birth_lb_frame = tk.Frame(date_birth_frame)
    date_birth_lb_frame.pack()

    date_birth_lb = tk.Listbox(date_birth_lb_frame, exportselection=False)
    date_birth_lb.pack(side=tk.LEFT, fill=tk.Y)

    date_birth_sb = tk.Scrollbar(date_birth_lb_frame)
    date_birth_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in df.columns:
        date_birth_lb.insert(tk.END, str(column))

    date_birth_sb.config(command=date_birth_lb.yview)
    date_birth_lb.config(yscrollcommand=date_birth_sb.set)

    #####

    rules_fixing_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    rules_fixing_frame.grid(row=0, column=2)

    rules_fixing_txt = tk.Message(rules_fixing_frame, text="Select the columns to which rule fixing should be applied:", width=600-10)
    rules_fixing_txt.pack()

    rules_fixing_lb_frame = tk.Frame(rules_fixing_frame)
    rules_fixing_lb_frame.pack()

    rules_fixing_lb = tk.Listbox(rules_fixing_lb_frame, exportselection=False, selectmode="multiple")
    rules_fixing_lb.pack(side=tk.LEFT, fill=tk.Y)

    rules_fixing_sb = tk.Scrollbar(rules_fixing_lb_frame)
    rules_fixing_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in df.columns:
        rules_fixing_lb.insert(tk.END, str(column))

    rules_fixing_sb.config(command=rules_fixing_lb.yview)
    rules_fixing_lb.config(yscrollcommand=rules_fixing_sb.set)

    # rules_fixing_lb.activate(3) check if u can get rid of the underline when deselecting with this

    #####

    totals_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    totals_frame.grid(row=1, column=0)

    totals_txt = tk.Message(totals_frame, text="Select the columns that should be checked for 'Total':", width=600-10)
    totals_txt.pack()

    totals_lb_frame = tk.Frame(totals_frame)
    totals_lb_frame.pack()

    totals_lb = tk.Listbox(totals_lb_frame, exportselection=False, selectmode="multiple")
    totals_lb.pack(side=tk.LEFT, fill=tk.Y)

    totals_sb = tk.Scrollbar(totals_lb_frame)
    totals_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in df.columns:
        totals_lb.insert(tk.END, str(column))

    totals_sb.config(command=totals_lb.yview)
    totals_lb.config(yscrollcommand=totals_sb.set)

    #####

    to_copy_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    to_copy_frame.grid(row=1, column=1)

    to_copy_txt = tk.Message(to_copy_frame, text="Select the columns that are copied from the last totals row:", width=600-10)
    to_copy_txt.pack()

    to_copy_lb_frame = tk.Frame(to_copy_frame)
    to_copy_lb_frame.pack()

    to_copy_lb = tk.Listbox(to_copy_lb_frame, exportselection=False, selectmode="multiple")
    to_copy_lb.pack(side=tk.LEFT, fill=tk.Y)

    to_copy_sb = tk.Scrollbar(to_copy_lb_frame)
    to_copy_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in df.columns:
        to_copy_lb.insert(tk.END, str(column))

    to_copy_sb.config(command=to_copy_lb.yview)
    to_copy_lb.config(yscrollcommand=to_copy_sb.set)

    #####

    priority_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    priority_frame.grid(row=1, column=2)

    priority_txt = tk.Message(priority_frame, text="Arrange the priority of the values for rule-fixing:", width=600-10)
    priority_txt.pack()

    priority_lb_frame = tk.Frame(priority_frame)
    priority_lb_frame.pack(side=tk.LEFT, padx=4)

    priority_lb = tk.Listbox(priority_lb_frame, exportselection=False)
    priority_lb.pack(side=tk.LEFT, fill=tk.Y)

    priority_sb = tk.Scrollbar(priority_lb_frame)
    priority_sb.pack(side=tk.RIGHT, fill=tk.Y)

    for column in ['Yes', 'At Risk', 'No', "Not applicable", "Unknown"]:
        priority_lb.insert(tk.END, str(column))

    priority_sb.config(command=priority_lb.yview)
    priority_lb.config(yscrollcommand=priority_sb.set)

    priority_lb.select_set(0) # Set focus on the first item.
    priority_lb.event_generate("<<ListboxSelect>>")

    priority_btns_frame = tk.Frame(priority_frame)
    priority_btns_frame.pack(side=tk.RIGHT, padx=4)

    priority_add_btn = tk.Button(priority_btns_frame, text="Add new", command=lambda: priority_add(priority_lb))
    priority_add_btn.pack(pady=1.5)

    priority_remove_btn = tk.Button(priority_btns_frame, text="Remove selected", command=lambda: priority_remove(priority_lb))
    priority_remove_btn.pack(pady=1.5)

    priority_up_btn = tk.Button(priority_btns_frame, text="Move selected up", command=lambda: priority_up(priority_lb))
    priority_up_btn.pack(pady=1.5)

    priority_down_btn = tk.Button(priority_btns_frame, text="Move selected down", command=lambda: priority_down(priority_lb))
    priority_down_btn.pack(pady=1.5)

    priority_edit_btn = tk.Button(priority_btns_frame, text="Edit selected", command=lambda: priority_edit(priority_lb))
    priority_edit_btn.pack(pady=1.5)

    #####

    process_customise_btn = tk.Button(root, text="Process using the above settings",
                                      command=lambda: process_customise(client_id_lb, date_birth_lb, rules_fixing_lb, totals_lb, to_copy_lb, priority_lb))
    process_customise_btn.grid(row=2, column=1, pady=10)

def edit_defaults_btn_pressed():
    for child in root.winfo_children():
        child.destroy()

    pass

if __name__ == '__main__':

    background_clr = '#c9c7c7'

    root = tk.Tk()
    root.title('Legal Data Cleanup')
    root.resizable(False, False)
    root.geometry('900x600')
    root.configure(background=background_clr)

    filename = "None"

    msg = tk.Message(root, text="File chosen: " + filename, width=600-10, bg=background_clr, font=("Arial", 12))
    
    btn_process = tk.Button(root, text="Process using the defaults", command=process_btn_pressed, state="disabled")
    btn_customise = tk.Button(root, text="Customise", command=customise_btn_pressed, state="disabled")
    btn_edit_defaults = tk.Button(root, text="Edit the defaults", command=edit_defaults_btn_pressed, state="disabled")

    btn_open = tk.Button(root, text="Open file", command=lambda: open_file_btn_pressed(msg, btn_process, btn_customise, btn_edit_defaults))

    msg.pack(side=tk.TOP, pady=10, fill=tk.X)
    btn_open.pack(pady=1.5)
    btn_process.pack(pady=1.5)
    btn_customise.pack(pady=1.5)
    btn_edit_defaults.pack(pady=1.5)
    

root.mainloop()