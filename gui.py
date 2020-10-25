import tkinter as tk
import stock_gui
import os


### Load Window ##########################

def fill_list():
    for x in files:
        lb.insert(tk.END, x.split(".")[0])


def list_click(x):
    stock_gui.StockGUI(lb.get(lb.curselection())).launch()


win = tk.Tk()
win.title("PortfolioOptimization")
screen_height = win.winfo_screenheight()
screen_width = win.winfo_screenwidth()
win.minsize(int(screen_width / 5), int(screen_height / 3))
lb = tk.Listbox(win)
files = os.listdir("stkdata/")
lb.configure(justify=tk.CENTER)
fill_list()
lb.bind("<Double-1>", list_click)
lb.pack()
win.mainloop()

##########################################
