import tkinter as tk
from StartState import StartState
from Data import Data

# DATE HAS TO BE %d/%m/%Y FORMAT !!!

if __name__ == '__main__':

    background_clr = '#c9c7c7'

    # Create the window
    root = tk.Tk()
    root.title('Legal Data Cleanup')

    # Set a default window size
    root.geometry('950x470')
    root.configure(background=background_clr)

    # Create the data object that gets passed around to the new states
    # on state transition
    data = Data()
    data.filename = "None"
    data.background_clr = background_clr

    # Create an instance of the starting state and "run" it
    state = StartState(data)
    state.enter(root)

    root.mainloop()