import tkinter as tk
from StartState import StartState
from Data import Data

# FIX THAT PROCESSING A PROCESSED FILE DOESNT WORK BECAUSE OF THE DATE TIME THING WITH DATE OF BIRTH

if __name__ == '__main__':

    background_clr = '#c9c7c7'

    root = tk.Tk()
    root.title('Legal Data Cleanup')
    #root.resizable(False, False)
    root.geometry('950x470')
    root.configure(background=background_clr)

    data = Data()
    data.filename = "None"
    data.background_clr = background_clr

    state = StartState(data)
    state.enter(root)

    root.mainloop()